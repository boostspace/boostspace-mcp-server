import requests

from .config import API_BASE, TOKEN


class BoostSpaceClient:

    def __init__(self, api_base: str = API_BASE, token: str = TOKEN):
        self.base = api_base.rstrip("/")
        self.headers = {"Authorization": f"Bearer {token}"}

    def request(self, method: str, path: str, params: dict = None, json_body: dict = None) -> dict:
        url = self.base + path
        resp = requests.request(method, url, params=params, json=json_body, headers=self.headers)
        resp.raise_for_status()
        return resp.json()
