from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from wolper_google.auth import AuthConfig
from wolper_google import http

CALENDAR_API_BASE = "https://www.googleapis.com/calendar/v3"
CALENDAR_LIST_URL = f"{CALENDAR_API_BASE}/users/me/calendarList"


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


def get_calendar(auth: AuthConfig, calendar_id: str) -> Mapping[str, object]:
    url = _calendar_url(f"/calendars/{calendar_id}")
    return http.get_json(url, auth.access_token)


def list_acl(
    auth: AuthConfig,
    calendar_id: str,
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _calendar_url(f"/calendars/{calendar_id}/acl")
    return http.get_json(url, auth.access_token, params=params)


def get_acl(auth: AuthConfig, calendar_id: str, rule_id: str) -> Mapping[str, object]:
    url = _calendar_url(f"/calendars/{calendar_id}/acl/{rule_id}")
    return http.get_json(url, auth.access_token)


def list_events(
    auth: AuthConfig,
    calendar_id: str,
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _calendar_url(f"/calendars/{calendar_id}/events")
    return http.get_json(url, auth.access_token, params=params)


def get_event(
    auth: AuthConfig,
    calendar_id: str,
    event_id: str,
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _calendar_url(f"/calendars/{calendar_id}/events/{event_id}")
    return http.get_json(url, auth.access_token, params=params)


def list_event_instances(
    auth: AuthConfig,
    calendar_id: str,
    event_id: str,
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> Mapping[str, object]:
    url = _calendar_url(f"/calendars/{calendar_id}/events/{event_id}/instances")
    return http.get_json(url, auth.access_token, params=params)


def get_colors(auth: AuthConfig) -> Mapping[str, object]:
    url = _calendar_url("/colors")
    return http.get_json(url, auth.access_token)


def get_calendar_list_entry(auth: AuthConfig, calendar_id: str) -> Mapping[str, object]:
    url = _calendar_url(f"/users/me/calendarList/{calendar_id}")
    return http.get_json(url, auth.access_token)


def list_settings(auth: AuthConfig) -> Mapping[str, object]:
    url = _calendar_url("/users/me/settings")
    return http.get_json(url, auth.access_token)


def get_setting(auth: AuthConfig, setting: str) -> Mapping[str, object]:
    url = _calendar_url(f"/users/me/settings/{setting}")
    return http.get_json(url, auth.access_token)


def _calendar_url(path: str) -> str:
    return f"{CALENDAR_API_BASE}{path}"
