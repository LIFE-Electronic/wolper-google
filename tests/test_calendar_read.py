from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from wolper_google import calendar, http
from wolper_google.auth import AuthConfig


def _auth() -> AuthConfig:
    return AuthConfig(
        access_token="token",
        expires_at=datetime(2026, 2, 20, 16, 55, 9, 859080, tzinfo=timezone.utc),
        token_type="Bearer",
    )


def _capture(monkeypatch) -> dict[str, Any]:
    called: dict[str, Any] = {}

    def fake_get_json(url: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        called["url"] = url
        called["token"] = token
        called["params"] = params
        return {"ok": True}

    monkeypatch.setattr(http, "get_json", fake_get_json)
    return called


def test_get_calendar(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.get_calendar(auth, "cal_1")

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/calendars/cal_1")
    assert called["token"] == "token"
    assert called["params"] is None


def test_get_calendar_list_entry(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.get_calendar_list_entry(auth, "cal_1")

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/users/me/calendarList/cal_1")


def test_list_acl_with_params(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)
    params = {"maxResults": "10"}

    payload = calendar.list_acl(auth, "cal_1", params=params)

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/calendars/cal_1/acl")
    assert called["params"] == params


def test_get_acl(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.get_acl(auth, "cal_1", "rule_1")

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/calendars/cal_1/acl/rule_1")


def test_list_events_with_params(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)
    params = {"timeMin": "2026-01-01T00:00:00Z"}

    payload = calendar.list_events(auth, "cal_1", params=params)

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/calendars/cal_1/events")
    assert called["params"] == params


def test_get_event(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.get_event(auth, "cal_1", "event_1")

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/calendars/cal_1/events/event_1")


def test_list_event_instances(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.list_event_instances(auth, "cal_1", "event_1")

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/calendars/cal_1/events/event_1/instances")


def test_get_colors(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.get_colors(auth)

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/colors")


def test_list_settings(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.list_settings(auth)

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/users/me/settings")


def test_get_setting(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = calendar.get_setting(auth, "locale")

    assert payload == {"ok": True}
    assert called["url"].endswith("/calendar/v3/users/me/settings/locale")
