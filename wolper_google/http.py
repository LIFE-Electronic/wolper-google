from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def get_json(
    url: str,
    token: str,
    params: Mapping[str, Sequence[str] | str] | None = None,
) -> dict[str, Any]:
    request_url = build_url(url, params)
    request = Request(request_url, headers={"Authorization": f"Bearer {token}"})
    with urlopen(request, timeout=20) as response:
        payload = response.read().decode("utf-8")
    data = json.loads(payload)
    if not isinstance(data, dict):
        message = "Expected JSON object response"
        raise ValueError(message)
    return data


def build_url(url: str, params: Mapping[str, Sequence[str] | str] | None) -> str:
    if not params:
        return url
    normalized: list[tuple[str, str]] = []
    for key, value in params.items():
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            for item in value:
                normalized.append((key, str(item)))
        else:
            normalized.append((key, str(value)))
    query = urlencode(normalized, doseq=True)
    return f"{url}?{query}"
