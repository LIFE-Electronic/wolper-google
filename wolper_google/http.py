from __future__ import annotations

import json
from typing import Any
from urllib.request import Request, urlopen


def get_json(url: str, token: str) -> dict[str, Any]:
    request = Request(url, headers={"Authorization": f"Bearer {token}"})
    with urlopen(request, timeout=20) as response:
        payload = response.read().decode("utf-8")
    data = json.loads(payload)
    if not isinstance(data, dict):
        message = "Expected JSON object response"
        raise ValueError(message)
    return data
