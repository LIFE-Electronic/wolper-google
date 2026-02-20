from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

from wolper_google.auth import AuthConfig
from wolper_google.calendar import Calendar
from wolper_google.gmail import Mailbox
from wolper_google.main import main


def _auth(tmp_path) -> tuple[AuthConfig, str]:
    auth_path = tmp_path / "auth.json"
    payload = {
        "access_token": "token",
        "expires_at": "2026-02-20T16:55:09.859080+00:00",
        "token_type": "Bearer",
    }
    auth_path.write_text(json.dumps(payload), encoding="utf-8")
    auth = AuthConfig(
        access_token="token",
        expires_at=datetime(2026, 2, 20, 16, 55, 9, 859080, tzinfo=timezone.utc),
        token_type="Bearer",
    )
    return auth, str(auth_path)


def test_calendar_list_parses_items(monkeypatch, tmp_path) -> None:
    auth, _ = _auth(tmp_path)
    payload = {
        "items": [
            {"id": "cal_1", "summary": "Primary"},
            {"id": "cal_2", "summary": "Work"},
        ]
    }

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        assert "calendar" in url
        assert token == "token"
        assert params is None
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    items = list(Calendar.list(auth))

    assert items == [
        Calendar(calendar_id="cal_1", summary="Primary"),
        Calendar(calendar_id="cal_2", summary="Work"),
    ]


def test_gmail_list_parses_items(monkeypatch, tmp_path) -> None:
    auth, _ = _auth(tmp_path)
    payload = {"labels": [{"id": "INBOX", "name": "Inbox"}]}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        assert "gmail" in url
        assert token == "token"
        assert params is None
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    items = list(Mailbox.list(auth))

    assert items == [Mailbox(mailbox_id="INBOX", name="Inbox")]


def test_cli_calendar_list(monkeypatch, tmp_path, capsys) -> None:
    _, auth_path = _auth(tmp_path)
    payload = {"items": [{"id": "cal_1", "summary": "Primary"}]}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    exit_code = main(["--auth-file", auth_path, "calendar", "list"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "cal_1\tPrimary"


def test_cli_gmail_list(monkeypatch, tmp_path, capsys) -> None:
    _, auth_path = _auth(tmp_path)
    payload = {"labels": [{"id": "INBOX", "name": "Inbox"}]}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    exit_code = main(["--auth-file", auth_path, "gmail", "list"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "INBOX\tInbox"


def test_cli_gmail_list_auth_after_subcommand(monkeypatch, tmp_path, capsys) -> None:
    _, auth_path = _auth(tmp_path)
    payload = {"labels": [{"id": "INBOX", "name": "Inbox"}]}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    exit_code = main(["gmail", "list", "--auth-file", auth_path])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == "INBOX\tInbox"


def test_cli_calendar_list_raw(monkeypatch, tmp_path, capsys) -> None:
    _, auth_path = _auth(tmp_path)
    payload = {"items": [{"id": "cal_1", "summary": "Primary"}]}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    exit_code = main(["--raw", "--auth-file", auth_path, "calendar", "list"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == json.dumps(payload, sort_keys=True)


def test_cli_gmail_list_raw_after_subcommand(monkeypatch, tmp_path, capsys) -> None:
    _, auth_path = _auth(tmp_path)
    payload = {"labels": [{"id": "INBOX", "name": "Inbox"}]}

    def fake_get_json(url: str, token: str) -> dict[str, Any]:
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    exit_code = main(["gmail", "list", "--raw", "--auth-file", auth_path])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == json.dumps(payload, sort_keys=True)
