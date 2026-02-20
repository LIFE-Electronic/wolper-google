from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Mapping, Sequence

from wolper_google import calendar as calendar_api
from wolper_google import gmail as gmail_api
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

    calendar_sub.add_parser("list", help="List calendars")

    calendar_get = calendar_sub.add_parser("get", help="Get calendar metadata")
    calendar_get.add_argument("--calendar-id", required=True)

    calendar_calendarlist = calendar_sub.add_parser("calendarlist", help="Calendar list entries")
    calendar_calendarlist_sub = calendar_calendarlist.add_subparsers(
        dest="calendarlist_command",
        required=True,
    )
    calendar_calendarlist_sub.add_parser("list", help="List calendar entries")
    calendar_calendarlist_get = calendar_calendarlist_sub.add_parser(
        "get",
        help="Get calendar list entry",
    )
    calendar_calendarlist_get.add_argument("--calendar-id", required=True)

    calendar_acl = calendar_sub.add_parser("acl", help="Calendar ACLs")
    calendar_acl_sub = calendar_acl.add_subparsers(dest="acl_command", required=True)
    calendar_acl_list = calendar_acl_sub.add_parser("list", help="List ACL rules")
    calendar_acl_list.add_argument("--calendar-id", required=True)
    _add_param_argument(calendar_acl_list)
    calendar_acl_get = calendar_acl_sub.add_parser("get", help="Get ACL rule")
    calendar_acl_get.add_argument("--calendar-id", required=True)
    calendar_acl_get.add_argument("--rule-id", required=True)

    calendar_events = calendar_sub.add_parser("events", help="Calendar events")
    calendar_events_sub = calendar_events.add_subparsers(dest="events_command", required=True)
    calendar_events_list = calendar_events_sub.add_parser("list", help="List events")
    calendar_events_list.add_argument("--calendar-id", required=True)
    _add_param_argument(calendar_events_list)
    calendar_events_get = calendar_events_sub.add_parser("get", help="Get event")
    calendar_events_get.add_argument("--calendar-id", required=True)
    calendar_events_get.add_argument("--event-id", required=True)
    _add_param_argument(calendar_events_get)
    calendar_events_instances = calendar_events_sub.add_parser(
        "instances",
        help="List event instances",
    )
    calendar_events_instances.add_argument("--calendar-id", required=True)
    calendar_events_instances.add_argument("--event-id", required=True)
    _add_param_argument(calendar_events_instances)

    calendar_colors = calendar_sub.add_parser("colors", help="Calendar colors")
    calendar_colors_sub = calendar_colors.add_subparsers(dest="colors_command", required=True)
    calendar_colors_sub.add_parser("get", help="Get colors")

    calendar_settings = calendar_sub.add_parser("settings", help="Calendar settings")
    calendar_settings_sub = calendar_settings.add_subparsers(
        dest="settings_command",
        required=True,
    )
    calendar_settings_sub.add_parser("list", help="List settings")
    calendar_setting_get = calendar_settings_sub.add_parser("get", help="Get setting")
    calendar_setting_get.add_argument("--setting", required=True)

    gmail_parent = argparse.ArgumentParser(add_help=False)
    gmail_parent.add_argument(
        "--user-id",
        default="me",
        help="Gmail user id (default: me)",
    )

    gmail_parser = subparsers.add_parser("gmail", help="Gmail commands", parents=[gmail_parent])
    gmail_sub = gmail_parser.add_subparsers(dest="command", required=True)

    gmail_sub.add_parser("list", help="List mailboxes", parents=[gmail_parent])

    gmail_labels = gmail_sub.add_parser("labels", help="Label commands", parents=[gmail_parent])
    gmail_labels_sub = gmail_labels.add_subparsers(dest="labels_command", required=True)
    gmail_labels_sub.add_parser("list", help="List labels", parents=[gmail_parent])
    gmail_labels_get = gmail_labels_sub.add_parser("get", help="Get label", parents=[gmail_parent])
    gmail_labels_get.add_argument("--label-id", required=True)

    gmail_drafts = gmail_sub.add_parser("drafts", help="Draft commands", parents=[gmail_parent])
    gmail_drafts_sub = gmail_drafts.add_subparsers(dest="drafts_command", required=True)
    gmail_drafts_list = gmail_drafts_sub.add_parser("list", help="List drafts", parents=[gmail_parent])
    _add_param_argument(gmail_drafts_list)
    gmail_drafts_get = gmail_drafts_sub.add_parser("get", help="Get draft", parents=[gmail_parent])
    gmail_drafts_get.add_argument("--draft-id", required=True)
    _add_param_argument(gmail_drafts_get)

    gmail_history = gmail_sub.add_parser("history", help="History commands", parents=[gmail_parent])
    gmail_history_sub = gmail_history.add_subparsers(dest="history_command", required=True)
    gmail_history_list = gmail_history_sub.add_parser("list", help="List history", parents=[gmail_parent])
    gmail_history_list.add_argument("--start-history-id", required=True)
    _add_param_argument(gmail_history_list)

    gmail_messages = gmail_sub.add_parser("messages", help="Message commands", parents=[gmail_parent])
    gmail_messages_sub = gmail_messages.add_subparsers(dest="messages_command", required=True)
    gmail_messages_list = gmail_messages_sub.add_parser(
        "list",
        help="List messages",
        parents=[gmail_parent],
    )
    _add_param_argument(gmail_messages_list)
    gmail_messages_get = gmail_messages_sub.add_parser("get", help="Get message", parents=[gmail_parent])
    gmail_messages_get.add_argument("--message-id", required=True)
    _add_param_argument(gmail_messages_get)

    gmail_attachments = gmail_sub.add_parser(
        "attachments",
        help="Attachment commands",
        parents=[gmail_parent],
    )
    gmail_attachments_sub = gmail_attachments.add_subparsers(
        dest="attachments_command",
        required=True,
    )
    gmail_attachments_get = gmail_attachments_sub.add_parser(
        "get",
        help="Get attachment",
        parents=[gmail_parent],
    )
    gmail_attachments_get.add_argument("--message-id", required=True)
    gmail_attachments_get.add_argument("--attachment-id", required=True)

    gmail_profile = gmail_sub.add_parser("profile", help="Profile commands", parents=[gmail_parent])
    gmail_profile_sub = gmail_profile.add_subparsers(dest="profile_command", required=True)
    gmail_profile_sub.add_parser("get", help="Get profile", parents=[gmail_parent])

    gmail_settings = gmail_sub.add_parser("settings", help="Settings commands", parents=[gmail_parent])
    gmail_settings_sub = gmail_settings.add_subparsers(dest="settings_command", required=True)

    settings_auto = gmail_settings_sub.add_parser(
        "auto-forwarding",
        help="Auto-forwarding settings",
        parents=[gmail_parent],
    )
    settings_auto_sub = settings_auto.add_subparsers(dest="auto_command", required=True)
    settings_auto_sub.add_parser(
        "get",
        help="Get auto-forwarding settings",
        parents=[gmail_parent],
    )

    settings_filters = gmail_settings_sub.add_parser(
        "filters",
        help="Filter settings",
        parents=[gmail_parent],
    )
    settings_filters_sub = settings_filters.add_subparsers(dest="filters_command", required=True)
    settings_filters_sub.add_parser("list", help="List filters", parents=[gmail_parent])
    settings_filters_get = settings_filters_sub.add_parser(
        "get",
        help="Get filter",
        parents=[gmail_parent],
    )
    settings_filters_get.add_argument("--filter-id", required=True)

    settings_forwarding = gmail_settings_sub.add_parser(
        "forwarding-addresses",
        help="Forwarding addresses",
        parents=[gmail_parent],
    )
    settings_forwarding_sub = settings_forwarding.add_subparsers(
        dest="forwarding_command",
        required=True,
    )
    settings_forwarding_sub.add_parser(
        "list",
        help="List forwarding addresses",
        parents=[gmail_parent],
    )
    settings_forwarding_get = settings_forwarding_sub.add_parser(
        "get",
        help="Get forwarding address",
        parents=[gmail_parent],
    )
    settings_forwarding_get.add_argument("--forwarding-email", required=True)

    settings_imap = gmail_settings_sub.add_parser("imap", help="IMAP settings", parents=[gmail_parent])
    settings_imap_sub = settings_imap.add_subparsers(dest="imap_command", required=True)
    settings_imap_sub.add_parser("get", help="Get IMAP settings", parents=[gmail_parent])

    settings_pop = gmail_settings_sub.add_parser("pop", help="POP settings", parents=[gmail_parent])
    settings_pop_sub = settings_pop.add_subparsers(dest="pop_command", required=True)
    settings_pop_sub.add_parser("get", help="Get POP settings", parents=[gmail_parent])

    settings_send_as = gmail_settings_sub.add_parser(
        "send-as",
        help="Send-as settings",
        parents=[gmail_parent],
    )
    settings_send_as_sub = settings_send_as.add_subparsers(dest="send_as_command", required=True)
    settings_send_as_sub.add_parser(
        "list",
        help="List send-as aliases",
        parents=[gmail_parent],
    )
    settings_send_as_get = settings_send_as_sub.add_parser(
        "get",
        help="Get send-as alias",
        parents=[gmail_parent],
    )
    settings_send_as_get.add_argument("--send-as-email", required=True)

    settings_smime = gmail_settings_sub.add_parser(
        "smime",
        help="S/MIME settings",
        parents=[gmail_parent],
    )
    settings_smime_sub = settings_smime.add_subparsers(dest="smime_command", required=True)
    settings_smime_list = settings_smime_sub.add_parser(
        "list",
        help="List S/MIME info",
        parents=[gmail_parent],
    )
    settings_smime_list.add_argument("--send-as-email", required=True)
    settings_smime_get = settings_smime_sub.add_parser(
        "get",
        help="Get S/MIME info",
        parents=[gmail_parent],
    )
    settings_smime_get.add_argument("--send-as-email", required=True)
    settings_smime_get.add_argument("--smime-id", required=True)

    settings_vacation = gmail_settings_sub.add_parser(
        "vacation",
        help="Vacation settings",
        parents=[gmail_parent],
    )
    settings_vacation_sub = settings_vacation.add_subparsers(
        dest="vacation_command",
        required=True,
    )
    settings_vacation_sub.add_parser(
        "get",
        help="Get vacation settings",
        parents=[gmail_parent],
    )

    gmail_threads = gmail_sub.add_parser("threads", help="Thread commands", parents=[gmail_parent])
    gmail_threads_sub = gmail_threads.add_subparsers(dest="threads_command", required=True)
    gmail_threads_list = gmail_threads_sub.add_parser("list", help="List threads", parents=[gmail_parent])
    _add_param_argument(gmail_threads_list)
    gmail_threads_get = gmail_threads_sub.add_parser("get", help="Get thread", parents=[gmail_parent])
    gmail_threads_get.add_argument("--thread-id", required=True)

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
        return _render_calendar_list(payload, args.raw)

    if args.service == "calendar" and args.command == "get":
        payload = calendar_api.get_calendar(auth, args.calendar_id)
        _print_json(payload)
        return 0

    if args.service == "calendar" and args.command == "calendarlist":
        if args.calendarlist_command == "list":
            payload = Calendar.list_raw(auth)
            return _render_calendar_list(payload, args.raw)
        if args.calendarlist_command == "get":
            payload = calendar_api.get_calendar_list_entry(auth, args.calendar_id)
            _print_json(payload)
            return 0

    if args.service == "calendar" and args.command == "acl":
        if args.acl_command == "list":
            params = _parse_params(args.param)
            payload = calendar_api.list_acl(auth, args.calendar_id, params=params)
            _print_json(payload)
            return 0
        if args.acl_command == "get":
            payload = calendar_api.get_acl(auth, args.calendar_id, args.rule_id)
            _print_json(payload)
            return 0

    if args.service == "calendar" and args.command == "events":
        if args.events_command == "list":
            params = _parse_params(args.param)
            payload = calendar_api.list_events(auth, args.calendar_id, params=params)
            _print_json(payload)
            return 0
        if args.events_command == "get":
            params = _parse_params(args.param)
            payload = calendar_api.get_event(auth, args.calendar_id, args.event_id, params=params)
            _print_json(payload)
            return 0
        if args.events_command == "instances":
            params = _parse_params(args.param)
            payload = calendar_api.list_event_instances(
                auth,
                args.calendar_id,
                args.event_id,
                params=params,
            )
            _print_json(payload)
            return 0

    if args.service == "calendar" and args.command == "colors":
        if args.colors_command == "get":
            payload = calendar_api.get_colors(auth)
            _print_json(payload)
            return 0

    if args.service == "calendar" and args.command == "settings":
        if args.settings_command == "list":
            payload = calendar_api.list_settings(auth)
            _print_json(payload)
            return 0
        if args.settings_command == "get":
            payload = calendar_api.get_setting(auth, args.setting)
            _print_json(payload)
            return 0

    if args.service == "gmail" and args.command == "list":
        payload = gmail_api.list_labels(auth, user_id=args.user_id)
        return _render_mailbox_list(payload, args.raw)

    if args.service == "gmail" and args.command == "labels":
        if args.labels_command == "list":
            payload = gmail_api.list_labels(auth, user_id=args.user_id)
            return _render_mailbox_list(payload, args.raw)
        if args.labels_command == "get":
            payload = gmail_api.get_label(auth, args.label_id, user_id=args.user_id)
            _print_json(payload)
            return 0

    if args.service == "gmail" and args.command == "drafts":
        if args.drafts_command == "list":
            params = _parse_params(args.param)
            payload = gmail_api.list_drafts(auth, user_id=args.user_id, params=params)
            _print_json(payload)
            return 0
        if args.drafts_command == "get":
            params = _parse_params(args.param)
            payload = gmail_api.get_draft(auth, args.draft_id, user_id=args.user_id)
            _print_json(payload)
            return 0

    if args.service == "gmail" and args.command == "history":
        if args.history_command == "list":
            params = _parse_params(args.param)
            payload = gmail_api.list_history(
                auth,
                start_history_id=args.start_history_id,
                user_id=args.user_id,
                params=params,
            )
            _print_json(payload)
            return 0

    if args.service == "gmail" and args.command == "messages":
        if args.messages_command == "list":
            params = _parse_params(args.param)
            payload = gmail_api.list_messages(auth, user_id=args.user_id, params=params)
            _print_json(payload)
            return 0
        if args.messages_command == "get":
            params = _parse_params(args.param)
            payload = gmail_api.get_message(
                auth,
                args.message_id,
                user_id=args.user_id,
                params=params,
            )
            _print_json(payload)
            return 0

    if args.service == "gmail" and args.command == "attachments":
        if args.attachments_command == "get":
            payload = gmail_api.get_message_attachment(
                auth,
                args.message_id,
                args.attachment_id,
                user_id=args.user_id,
            )
            _print_json(payload)
            return 0

    if args.service == "gmail" and args.command == "profile":
        if args.profile_command == "get":
            payload = gmail_api.get_profile(auth, user_id=args.user_id)
            _print_json(payload)
            return 0

    if args.service == "gmail" and args.command == "settings":
        if args.settings_command == "auto-forwarding":
            if args.auto_command == "get":
                payload = gmail_api.get_settings_auto_forwarding(auth, user_id=args.user_id)
                _print_json(payload)
                return 0
        if args.settings_command == "filters":
            if args.filters_command == "list":
                payload = gmail_api.list_settings_filters(auth, user_id=args.user_id)
                _print_json(payload)
                return 0
            if args.filters_command == "get":
                payload = gmail_api.get_settings_filter(
                    auth,
                    args.filter_id,
                    user_id=args.user_id,
                )
                _print_json(payload)
                return 0
        if args.settings_command == "forwarding-addresses":
            if args.forwarding_command == "list":
                payload = gmail_api.list_settings_forwarding_addresses(
                    auth,
                    user_id=args.user_id,
                )
                _print_json(payload)
                return 0
            if args.forwarding_command == "get":
                payload = gmail_api.get_settings_forwarding_address(
                    auth,
                    args.forwarding_email,
                    user_id=args.user_id,
                )
                _print_json(payload)
                return 0
        if args.settings_command == "imap":
            if args.imap_command == "get":
                payload = gmail_api.get_settings_imap(auth, user_id=args.user_id)
                _print_json(payload)
                return 0
        if args.settings_command == "pop":
            if args.pop_command == "get":
                payload = gmail_api.get_settings_pop(auth, user_id=args.user_id)
                _print_json(payload)
                return 0
        if args.settings_command == "send-as":
            if args.send_as_command == "list":
                payload = gmail_api.list_settings_send_as(auth, user_id=args.user_id)
                _print_json(payload)
                return 0
            if args.send_as_command == "get":
                payload = gmail_api.get_settings_send_as(
                    auth,
                    args.send_as_email,
                    user_id=args.user_id,
                )
                _print_json(payload)
                return 0
        if args.settings_command == "smime":
            if args.smime_command == "list":
                payload = gmail_api.list_settings_smime_info(
                    auth,
                    args.send_as_email,
                    user_id=args.user_id,
                )
                _print_json(payload)
                return 0
            if args.smime_command == "get":
                payload = gmail_api.get_settings_smime_info(
                    auth,
                    args.send_as_email,
                    args.smime_id,
                    user_id=args.user_id,
                )
                _print_json(payload)
                return 0
        if args.settings_command == "vacation":
            if args.vacation_command == "get":
                payload = gmail_api.get_settings_vacation(auth, user_id=args.user_id)
                _print_json(payload)
                return 0

    if args.service == "gmail" and args.command == "threads":
        if args.threads_command == "list":
            params = _parse_params(args.param)
            payload = gmail_api.list_threads(auth, user_id=args.user_id, params=params)
            _print_json(payload)
            return 0
        if args.threads_command == "get":
            payload = gmail_api.get_thread(auth, args.thread_id, user_id=args.user_id)
            _print_json(payload)
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


def _parse_params(pairs: Sequence[str] | None) -> dict[str, list[str] | str] | None:
    if not pairs:
        return None
    params: dict[str, list[str] | str] = {}
    for pair in pairs:
        if "=" not in pair:
            message = f"Invalid param format: {pair}. Expected key=value."
            raise ValueError(message)
        key, value = pair.split("=", 1)
        if key in params:
            existing = params[key]
            if isinstance(existing, list):
                existing.append(value)
            else:
                params[key] = [existing, value]
        else:
            params[key] = value
    return params


def _add_param_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--param",
        action="append",
        help="Query parameter (key=value). Repeatable.",
    )


def _render_calendar_list(payload: Mapping[str, object], raw: bool) -> int:
    if raw:
        _print_json(payload)
        return 0
    for item in Calendar.list_from_payload(payload):
        print(f"{item.calendar_id}\t{item.summary}")
    return 0


def _render_mailbox_list(payload: Mapping[str, object], raw: bool) -> int:
    if raw:
        _print_json(payload)
        return 0
    for item in Mailbox.list_from_payload(payload):
        print(f"{item.mailbox_id}\t{item.name}")
    return 0


def _print_json(payload: Mapping[str, object]) -> None:
    print(json.dumps(payload, sort_keys=True))
