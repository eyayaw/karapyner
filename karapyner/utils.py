from typing import Any


def open_app(name: str) -> dict[str, Any]:
    """Helper to create app-opening action"""
    return {
        "description": f"Open {name}",
        "to": [{"shell_command": f"open -a '{name}.app'"}],
    }


def open_url(url: str) -> dict[str, Any]:
    """Helper to create URL-opening action"""
    return {"description": f"Open {url}", "to": [{"shell_command": f"open '{url}'"}]}


def open_raycast_deeplink(link: str) -> dict[str, Any]:
    """Helper to open Raycast deeplink"""
    return {
        "description": f"Window: {link.split("/")[-1].replace('-', ' ').title()}",
        "to": [{"shell_command": f"open -g '{link}'"}],
    }
