from __future__ import annotations

import json
import os
import time
from pathlib import Path

import requests

OPENAPI_SOURCE_URL = "https://apidoc.boost.space/latest.json"

_default_cache = (
    Path(os.getenv("XDG_CACHE_HOME", Path.home() / ".cache"))
    if os.name != "nt"
    else Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
)
CACHE_DIR = _default_cache / "boostspace-mcp"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

OPENAPI_JSON = CACHE_DIR / "latest.json"


def refresh_openapi_cache(ttl_hours: int = 24) -> Path:
    if OPENAPI_JSON.exists():
        age_hours = (time.time() - OPENAPI_JSON.stat().st_mtime) / 3600
        if age_hours < ttl_hours:
            return OPENAPI_JSON

    resp = requests.get(OPENAPI_SOURCE_URL, timeout=15)
    resp.raise_for_status()
    OPENAPI_JSON.write_bytes(resp.content)

    try:
        json.loads(resp.text)
    except json.JSONDecodeError:
        OPENAPI_JSON.unlink(missing_ok=True)
        raise RuntimeError("Downloaded OPEN API docs are not valid JSON.")

    return OPENAPI_JSON


__all__ = ["OPENAPI_JSON", "refresh_openapi_cache"]
