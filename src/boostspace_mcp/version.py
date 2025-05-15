from __future__ import annotations

from importlib import metadata as importlib_metadata


def get_version() -> str:
    try:
        return importlib_metadata.version("boostspace-mcp")
    except importlib_metadata.PackageNotFoundError:
        return "0.0.0+dev"

SERVER_VERSION: str = get_version()

__all__ = ["get_version", "SERVER_VERSION"]
