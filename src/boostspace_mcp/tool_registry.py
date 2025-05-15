from __future__ import annotations

import re

from .api_client import BoostSpaceClient
from .config import ALLOWED_ENDPOINTS
from .spec_loader import load_openapi_spec


class ToolRegistry:
    def __init__(self, mcp, client: BoostSpaceClient):
        self.mcp = mcp
        self.client = client
        self._used_names: set[str] = set()

    def _fill_path(self, template: str, parameters: dict) -> tuple[str, dict]:
        extras = parameters.copy()
        for key, value in list(parameters.items()):
            placeholder = f"{{{key}}}"
            if placeholder in template:
                template = template.replace(placeholder, str(value))
                extras.pop(key)
        return template, extras

    @staticmethod
    def _generate_tool_id(method: str, path: str) -> str:
        cleaned = (
            path.strip("/")
            .replace("/", "_")
            .translate(str.maketrans("", "", "{}"))
        )
        return f"{method.lower()}_{cleaned}"

    def _sanitize_name(self, raw: str) -> str:
        """
        Return a unique MCP-safe tool name:
        - only [a-zA-Z0-9_-]
        - ≤ 64 chars *including* any suffix
        """

        name = re.sub(r"[^a-zA-Z0-9_-]", "_", raw)
        name = re.sub(r"_+", "_", name).strip("_") or "tool"

        base = name
        i = 2
        while name in self._used_names:
            suffix = f"_{i}"
            name = (base[: 64 - len(suffix)]) + suffix
            i += 1

        name = name[:64]
        self._used_names.add(name)
        return name

    def _register_tool(self, method: str, path: str, name: str, description: str):
        @self.mcp.tool(name=name, description=description)
        def endpoint_tool(args: dict) -> dict:
            try:
                filled_path, params = self._fill_path(path, args)
                if method.upper() == "GET":
                    return self.client.request(method, filled_path, params=params)
                return self.client.request(method, filled_path, json_body=params)
            except Exception as exc:
                return {"error": str(exc)}

        endpoint_tool.__name__ = name

    def register_all(self) -> None:
        spec = load_openapi_spec()

        if ALLOWED_ENDPOINTS:
            target = ALLOWED_ENDPOINTS
        else:
            target: list[str] = [
                f"{method.upper()} {path}"
                for path, methods in spec["paths"].items()
                for method in methods.keys()
            ]

        for entry in target:
            try:
                method, path = entry.strip().split(maxsplit=1)
            except ValueError:
                print(f"[warn] malformed ALLOWED_ENDPOINTS entry: {entry!r}")
                continue

            operation = spec["paths"].get(path, {}).get(method.lower())
            if not operation:
                print(f"[warn] {method} {path} skipped (not in spec)")
                continue

            pretty_name = operation.get("summary", "").strip() or path
            raw_tool_name = pretty_name.lower() or self._generate_tool_id(method, path)
            tool_name = self._sanitize_name(raw_tool_name)

            description = f"[{pretty_name}]"
            if "parameters" in operation:
                pieces = []
                for param in operation["parameters"]:
                    if "$ref" in param:
                        ref_name = param["$ref"].split("/")[-1]
                        param_def = spec["components"]["parameters"].get(ref_name, {})
                    else:
                        param_def = param

                    required = " (required)" if param_def.get("required") else " (optional)"
                    pieces.append(
                        f"{param_def.get('name', '?')}{required}: "
                        f"{param_def.get('description', 'No description')}"
                    )

                if pieces:
                    description += "\nargs:\n" + " | ".join(pieces)

            self._register_tool(method, path, tool_name, description)
