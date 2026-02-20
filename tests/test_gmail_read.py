from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from wolper_google import gmail, http
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


def test_list_drafts(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_drafts(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/drafts")


def test_get_draft(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_draft(auth, "draft_1", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/drafts/draft_1")


def test_list_history(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_history(auth, start_history_id="123", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/history")
    assert called["params"] == {"startHistoryId": "123"}


def test_list_labels(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_labels(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/labels")


def test_get_label(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_label(auth, "INBOX", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/labels/INBOX")


def test_list_messages(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)
    params = {"maxResults": "5"}

    payload = gmail.list_messages(auth, user_id="me", params=params)

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/messages")
    assert called["params"] == params


def test_get_message(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_message(auth, "msg_1", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/messages/msg_1")


def test_get_attachment(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_message_attachment(auth, "msg_1", "att_1", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/messages/msg_1/attachments/att_1")


def test_get_profile(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_profile(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/profile")


def test_get_settings_auto_forwarding(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_settings_auto_forwarding(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/autoForwarding")


def test_settings_filters(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_settings_filters(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/filters")

    payload = gmail.get_settings_filter(auth, "filter_1", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/filters/filter_1")


def test_settings_forwarding_addresses(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_settings_forwarding_addresses(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/forwardingAddresses")

    payload = gmail.get_settings_forwarding_address(auth, "user@example.com", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/forwardingAddresses/user@example.com")


def test_settings_imap_pop(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_settings_imap(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/imap")

    payload = gmail.get_settings_pop(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/pop")


def test_settings_send_as(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_settings_send_as(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/sendAs")

    payload = gmail.get_settings_send_as(auth, "me@example.com", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/sendAs/me@example.com")


def test_settings_smime(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_settings_smime_info(auth, "me@example.com", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/sendAs/me@example.com/smimeInfo")

    payload = gmail.get_settings_smime_info(auth, "me@example.com", "smime_1", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/sendAs/me@example.com/smimeInfo/smime_1")


def test_get_settings_vacation(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.get_settings_vacation(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/settings/vacation")


def test_threads(monkeypatch) -> None:
    auth = _auth()
    called = _capture(monkeypatch)

    payload = gmail.list_threads(auth, user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/threads")

    payload = gmail.get_thread(auth, "thread_1", user_id="me")

    assert payload == {"ok": True}
    assert called["url"].endswith("/gmail/v1/users/me/threads/thread_1")
