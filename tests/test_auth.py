from __future__ import annotations

from datetime import datetime, timezone
import json

from wolper_google.auth import read_auth_file


def test_read_auth_file_parses(tmp_path) -> None:
    auth_path = tmp_path / "auth.json"
    payload = {
        "access_token": "token",
        "expires_at": "2026-02-20T16:55:09.859080+00:00",
        "token_type": "Bearer",
    }
    auth_path.write_text(json.dumps(payload), encoding="utf-8")

    auth = read_auth_file(auth_path)

    assert auth.access_token == "token"
    assert auth.token_type == "Bearer"
    assert auth.expires_at == datetime(2026, 2, 20, 16, 55, 9, 859080, tzinfo=timezone.utc)
