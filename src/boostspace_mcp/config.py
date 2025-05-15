from __future__ import annotations

import os

SERVER_NAME      = "boostspace-mcp"
API_BASE: str | None = os.getenv("BOOSTSPACE_API_BASE")
TOKEN:    str | None = os.getenv("BOOSTSPACE_TOKEN")

ALLOWED_ENDPOINTS: list[str] = [] # Empty list  ⇒  allow every endpoint
# EXAMPLE of ALLOWED_ENDPOINTS values:
#    [
#        "GET    /custom-module",
#        "GET    /custom-module-item",
#    ]

if API_BASE is None:
    raise RuntimeError(
        "Missing required environment variable BOOSTSPACE_API_BASE.\n"
        "Set it in your MCP host application (e.g. Claude Desktop) before "
        "starting the server."
    )

if TOKEN is None:
    raise RuntimeError(
        "Missing required environment variable BOOSTSPACE_TOKEN.\n"
        "Set it in your MCP host application (e.g. Claude Desktop) before "
        "starting the server."
    )