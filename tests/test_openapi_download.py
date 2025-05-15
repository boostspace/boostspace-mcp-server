"""
Integration test: download the real OpenAPI spec and make sure it is cached
and valid JSON.
"""

import json

from boostspace_mcp.spec_cache import OPENAPI_JSON, refresh_openapi_cache


def test_openapi_real_download():
    path = refresh_openapi_cache(ttl_hours=0)
    assert path == OPENAPI_JSON and path.exists()
    assert path.stat().st_size > 0

    data = json.loads(path.read_text("utf-8"))
    assert "openapi" in data and "paths" in data
