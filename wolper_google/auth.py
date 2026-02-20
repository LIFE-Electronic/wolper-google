from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from typing import Any

DEFAULT_AUTH_FILE = Path("~/.googleauth.json")


@dataclass(frozen=True)
class AuthConfig:
    access_token: str
    expires_at: datetime
    token_type: str


def read_auth_file(path: str | Path | None = None) -> AuthConfig:
    auth_path = Path(path) if path is not None else DEFAULT_AUTH_FILE
    auth_path = auth_path.expanduser()

    raw = auth_path.read_text(encoding="utf-8")
    payload = json.loads(raw)

    access_token = _require_str(payload, "access_token")
    token_type = _require_str(payload, "token_type")
    expires_at_raw = _require_str(payload, "expires_at")

    try:
        expires_at = datetime.fromisoformat(expires_at_raw)
    except ValueError as exc:
        message = f"Invalid expires_at timestamp: {expires_at_raw}"
        raise ValueError(message) from exc

    return AuthConfig(
        access_token=access_token,
        expires_at=expires_at,
        token_type=token_type,
    )


def _require_str(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        message = f"Missing or invalid {key} in auth file"
        raise ValueError(message)
    return value
