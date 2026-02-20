from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from wolper_google.auth import read_auth_file
from wolper_google.calendar import Calendar
from wolper_google.gmail import Mailbox


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wolper-google")
    parser.add_argument(
        "--auth-file",
        dest="auth_file",
        type=str,
        default=None,
        help="Path to auth JSON (default: ~/.googleauth.json)",
    )
    parser.add_argument(
        "--raw",
        dest="raw",
        action="store_true",
        help="Print raw JSON response",
    )
    subparsers = parser.add_subparsers(dest="service", required=True)

    calendar_parser = subparsers.add_parser("calendar", help="Calendar commands")
    calendar_sub = calendar_parser.add_subparsers(dest="command", required=True)
    calendar_sub.add_parser(
        "list",
        help="List calendars",
    )

    gmail_parser = subparsers.add_parser("gmail", help="Gmail commands")
    gmail_sub = gmail_parser.add_subparsers(dest="command", required=True)
    gmail_sub.add_parser(
        "list",
        help="List mailboxes",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    raw_argv = list(sys.argv[1:]) if argv is None else list(argv)
    auth_file, raw_mode, cleaned_argv = _extract_global_flags(raw_argv)
    args = parser.parse_args(cleaned_argv)
    if auth_file is not None:
        args.auth_file = auth_file
    if raw_mode:
        args.raw = True

    try:
        auth = read_auth_file(Path(args.auth_file) if args.auth_file else None)
    except Exception as exc:  # noqa: BLE001
        print(f"Auth error: {exc}", file=sys.stderr)
        return 1

    if args.service == "calendar" and args.command == "list":
        payload = Calendar.list_raw(auth)
        if args.raw:
            print(json.dumps(payload, sort_keys=True))
        else:
            for item in Calendar.list_from_payload(payload):
                print(f"{item.calendar_id}\t{item.summary}")
        return 0

    if args.service == "gmail" and args.command == "list":
        payload = Mailbox.list_raw(auth)
        if args.raw:
            print(json.dumps(payload, sort_keys=True))
        else:
            for item in Mailbox.list_from_payload(payload):
                print(f"{item.mailbox_id}\t{item.name}")
        return 0

    print("Unknown command", file=sys.stderr)
    return 1


def cli() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    cli()


def _extract_global_flags(
    argv: Sequence[str] | None,
) -> tuple[str | None, bool, list[str] | None]:
    if argv is None:
        return None, None, None

    auth_file: str | None = None
    raw_mode = False
    cleaned: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--auth-file":
            if i + 1 < len(argv):
                auth_file = argv[i + 1]
                i += 2
                continue
        if arg.startswith("--auth-file="):
            auth_file = arg.split("=", 1)[1]
            i += 1
            continue
        if arg == "--raw":
            raw_mode = True
            i += 1
            continue
        cleaned.append(arg)
        i += 1
    return auth_file, raw_mode, cleaned
