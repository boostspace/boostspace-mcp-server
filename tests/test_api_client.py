import types

from boostspace_mcp.api_client import BoostSpaceClient


def test_request_builds_url_and_headers(monkeypatch):
    captured = {}

    def fake_request(method, url, params=None, json=None, headers=None):
        captured.update(method=method, url=url, params=params, json=json, headers=headers)

        resp = types.SimpleNamespace()
        resp.raise_for_status = lambda: None
        resp.json = lambda: {"ok": True}
        return resp

    monkeypatch.setattr("boostspace_mcp.api_client.requests.request", fake_request)

    client = BoostSpaceClient(api_base="https://example.com", token="tkn")
    data = client.request("GET", "/demo", params={"a": 1})

    assert data == {"ok": True}
    assert captured["url"] == "https://example.com/demo"
    assert captured["headers"]["Authorization"] == "Bearer tkn"
    assert captured["params"] == {"a": 1}
