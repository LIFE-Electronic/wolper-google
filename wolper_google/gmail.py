from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from wolper_google.auth import AuthConfig
from wolper_google import http

GMAIL_LABELS_URL = "https://gmail.googleapis.com/gmail/v1/users/me/labels"


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
