from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from wolper_google.auth import AuthConfig
from wolper_google import http

GMAIL_API_BASE = "https://gmail.googleapis.com/gmail/v1/users"
GMAIL_LABELS_URL = f"{GMAIL_API_BASE}/me/labels"


@dataclass(frozen=True)
class Mailbox:
    mailbox_id: str
    name: str

    @classmethod
    def list(cls, auth: AuthConfig) -> Iterable[Mailbox]:
        payload = cls.list_raw(auth)
        return cls.list_from_payload(payload)

    @classmethod
    def list_raw(cls, auth: AuthConfig) -> Mapping[str, object]:
        payload = http.get_json(GMAIL_LABELS_URL, auth.access_token)
        if not isinstance(payload, dict):
            message = "Invalid gmail labels response"
            raise ValueError(message)
        return payload

    @classmethod
    def list_from_payload(cls, payload: Mapping[str, object]) -> Iterable[Mailbox]:
        labels = payload.get("labels", [])
        if not isinstance(labels, Sequence):
            message = "Invalid gmail labels response"
            raise ValueError(message)
        for item in labels:
            if not isinstance(item, dict):
                continue
            mailbox_id = item.get("id")
            name = item.get("name", "")
            if isinstance(mailbox_id, str) and isinstance(name, str):
                yield cls(mailbox_id=mailbox_id, name=name)


def list_drafts(
    auth: AuthConfig,
    user_id: str = "me",
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _gmail_url(user_id, "/drafts")
    return http.get_json(url, auth.access_token, params=params)


def get_draft(auth: AuthConfig, draft_id: str, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/drafts/{draft_id}")
    return http.get_json(url, auth.access_token)


def list_history(
    auth: AuthConfig,
    start_history_id: str,
    user_id: str = "me",
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    merged_params: dict[str, Sequence[str] | str] = {}
    if params:
        merged_params.update(params)
    merged_params["startHistoryId"] = start_history_id
    url = _gmail_url(user_id, "/history")
    return http.get_json(url, auth.access_token, params=merged_params)


def list_labels(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/labels")
    return http.get_json(url, auth.access_token)


def get_label(auth: AuthConfig, label_id: str, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/labels/{label_id}")
    return http.get_json(url, auth.access_token)


def list_messages(
    auth: AuthConfig,
    user_id: str = "me",
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _gmail_url(user_id, "/messages")
    return http.get_json(url, auth.access_token, params=params)


def get_message(
    auth: AuthConfig,
    message_id: str,
    user_id: str = "me",
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/messages/{message_id}")
    return http.get_json(url, auth.access_token, params=params)


def get_message_attachment(
    auth: AuthConfig,
    message_id: str,
    attachment_id: str,
    user_id: str = "me",
) -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/messages/{message_id}/attachments/{attachment_id}")
    return http.get_json(url, auth.access_token)


def get_profile(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/profile")
    return http.get_json(url, auth.access_token)


def get_settings_auto_forwarding(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/settings/autoForwarding")
    return http.get_json(url, auth.access_token)


def list_settings_filters(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/settings/filters")
    return http.get_json(url, auth.access_token)


def get_settings_filter(auth: AuthConfig, filter_id: str, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/settings/filters/{filter_id}")
    return http.get_json(url, auth.access_token)


def list_settings_forwarding_addresses(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/settings/forwardingAddresses")
    return http.get_json(url, auth.access_token)


def get_settings_forwarding_address(
    auth: AuthConfig,
    forwarding_email: str,
    user_id: str = "me",
) -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/settings/forwardingAddresses/{forwarding_email}")
    return http.get_json(url, auth.access_token)


def get_settings_imap(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/settings/imap")
    return http.get_json(url, auth.access_token)


def get_settings_pop(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/settings/pop")
    return http.get_json(url, auth.access_token)


def list_settings_send_as(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/settings/sendAs")
    return http.get_json(url, auth.access_token)


def get_settings_send_as(
    auth: AuthConfig,
    send_as_email: str,
    user_id: str = "me",
) -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/settings/sendAs/{send_as_email}")
    return http.get_json(url, auth.access_token)


def list_settings_smime_info(
    auth: AuthConfig,
    send_as_email: str,
    user_id: str = "me",
) -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/settings/sendAs/{send_as_email}/smimeInfo")
    return http.get_json(url, auth.access_token)


def get_settings_smime_info(
    auth: AuthConfig,
    send_as_email: str,
    smime_id: str,
    user_id: str = "me",
) -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/settings/sendAs/{send_as_email}/smimeInfo/{smime_id}")
    return http.get_json(url, auth.access_token)


def get_settings_vacation(auth: AuthConfig, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, "/settings/vacation")
    return http.get_json(url, auth.access_token)


def list_threads(
    auth: AuthConfig,
    user_id: str = "me",
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _gmail_url(user_id, "/threads")
    return http.get_json(url, auth.access_token, params=params)


def get_thread(auth: AuthConfig, thread_id: str, user_id: str = "me") -> Mapping[str, object]:
    url = _gmail_url(user_id, f"/threads/{thread_id}")
    return http.get_json(url, auth.access_token)


def _gmail_url(user_id: str, path: str) -> str:
    return f"{GMAIL_API_BASE}/{user_id}{path}"
