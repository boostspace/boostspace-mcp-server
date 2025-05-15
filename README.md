# Boost.space MCP server

A Model Context Protocol (MCP) server proxying Boost.Space’s REST API for MCP clients (e.g., Claude Desktop).

## Install

**pip:**

```bash
pip install boostspace-mcp
```

**uv:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv add boostspace-mcp
```

## Run

```bash
# pip
python -m boostspace_mcp.server

# uv
uv x boostspace-mcp run
```

## Claude Desktop config

```jsonc
"mcpServers": {
  "boostspace": {
    "command": "python",
    "args": ["-m","boostspace_mcp.server"],
    "env": {
      "BOOSTSPACE_API_BASE": "{{API_PATH}}",
      "BOOSTSPACE_TOKEN": "{{TOKEN}}"
    },
    "transport": "stdio"
  }
}
```

Restart Claude Desktop.

## Env vars

- `BOOSTSPACE_API_BASE`: API base URL
- `BOOSTSPACE_TOKEN`: Bearer token

## Test & dev

```bash
pip install .[dev]
pytest -q
ruff check .
```
