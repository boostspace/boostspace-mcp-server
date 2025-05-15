from mcp.server.fastmcp import FastMCP

from .api_client import BoostSpaceClient
from .config import SERVER_NAME
from .tool_registry import ToolRegistry
from .version import SERVER_VERSION


def main():
    mcp = FastMCP(SERVER_NAME, version=SERVER_VERSION)
    client = BoostSpaceClient()
    registry = ToolRegistry(mcp, client)
    registry.register_all()
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
