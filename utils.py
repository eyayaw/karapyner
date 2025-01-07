from typing import Any


def open_app(name: str) -> dict:
    """Helper to create app-opening action"""
    return {
        "description": f"Open {name}",
        "to": [{"shell_command": f"open -a '{name}.app'"}],
    }


def open_url(url: str) -> dict:
    """Helper to create URL-opening action"""
    return {"description": f"Open {url}", "to": [{"shell_command": f"open '{url}'"}]}


def raycast_window(action: str) -> dict[str, Any]:
    """
    Create a Raycast window management action
    Args:
        action: String representing the window action
    Returns:
        Dict containing the Raycast action configuration
    """
    return {
        "description": f"Window: {action.replace('-', ' ').title()}",
        "to": [
            {
                "shell_command": f"open -g 'raycast://extensions/raycast/window-management/{action}'"
            }
        ],
    }


# Generate window management configuration
def window_mgt_config(window_mgt_mappings: dict[str, str]) -> dict:
    """
    Generate a Raycast window configuration
    Returns:
        Dict containing the Raycast window configuration
    """
    return {
        letter: raycast_window(action) for letter, action in window_mgt_mappings.items()
    }
