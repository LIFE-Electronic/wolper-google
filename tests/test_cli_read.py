from __future__ import annotations

from datetime import datetime, timezone
import json
from typing import Any

from wolper_google.auth import AuthConfig
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


def test_cli_calendar_events_list_raw(monkeypatch, tmp_path, capsys) -> None:
    _, auth_path = _auth(tmp_path)
    payload = {"items": [{"id": "event_1"}]}
    called: dict[str, Any] = {}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        called["url"] = url
        called["token"] = token
        called["params"] = params
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    exit_code = main(
        [
            "calendar",
            "events",
            "list",
            "--calendar-id",
            "cal_1",
            "--param",
            "maxResults=5",
            "--raw",
            "--auth-file",
            auth_path,
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert called["token"] == "token"
    assert called["params"] == {"maxResults": "5"}
    assert captured.out.strip() == json.dumps(payload, sort_keys=True)


def test_cli_gmail_messages_get_raw(monkeypatch, tmp_path, capsys) -> None:
    _, auth_path = _auth(tmp_path)
    payload = {"id": "msg_1"}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return payload

    from wolper_google import http

    monkeypatch.setattr(http, "get_json", fake_get_json)

    exit_code = main(
        [
            "gmail",
            "messages",
            "get",
            "--message-id",
            "msg_1",
            "--auth-file",
            auth_path,
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip() == json.dumps(payload, sort_keys=True)
