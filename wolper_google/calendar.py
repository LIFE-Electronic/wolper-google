from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from wolper_google.auth import AuthConfig
from wolper_google import http

CALENDAR_LIST_URL = "https://www.googleapis.com/calendar/v3/users/me/calendarList"


@dataclass(frozen=True)
class Calendar:
    calendar_id: str
    summary: str

    @classmethod
    def list(cls, auth: AuthConfig) -> Iterable[Calendar]:
        payload = cls.list_raw(auth)
        return cls.list_from_payload(payload)

    @classmethod
    def list_raw(cls, auth: AuthConfig) -> Mapping[str, object]:
        payload = http.get_json(CALENDAR_LIST_URL, auth.access_token)
        if not isinstance(payload, dict):
            message = "Invalid calendar list response"
            raise ValueError(message)
        return payload

    @classmethod
    def list_from_payload(cls, payload: Mapping[str, object]) -> Iterable[Calendar]:
        items = payload.get("items", [])
        if not isinstance(items, Sequence):
            message = "Invalid calendar list response"
            raise ValueError(message)
        for item in items:
            if not isinstance(item, dict):
                continue
            calendar_id = item.get("id")
            summary = item.get("summary", "")
            if isinstance(calendar_id, str) and isinstance(summary, str):
                yield cls(calendar_id=calendar_id, summary=summary)
