import json
from functools import lru_cache
from pathlib import Path

from .spec_cache import OPENAPI_JSON, refresh_openapi_cache


@lru_cache(maxsize=1)
def load_openapi_spec() -> dict:
    refresh_openapi_cache()
    text = Path(OPENAPI_JSON).read_text("utf-8")
    return json.loads(text)