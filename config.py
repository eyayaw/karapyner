from karabiner import KarabinerConfig
from utils import open_url, window_mgt_config

KARABINER_CONFIG_PATH = "karabiner.json"
TERMINAL_APP = "Ghostty"
BROWSER_APP = "Arc"

# Vim-style key mappings for Raycast window management actions
WINDOW_ACTIONS = {
    # Main positions (vim directions)
    "h": "left-half",  # Left
    "l": "right-half",  # Right
    "k": "top-half",  # Top
    "j": "bottom-half",  # Bottom
    # Corners (u = up corner, n = down corner)
    "u": "top-left-quarter",  # Top Left
    "i": "top-right-quarter",  # Top Right
    "n": "bottom-left-quarter",  # Bottom Left
    "m": "bottom-right-quarter",  # Bottom Right
    # Thirds (d = divided sections)
    "d": "first-third",  # Left Third
    "f": "center-third",  # Center Third
    "g": "last-third",  # Right Third
    # Two Thirds
    "e": "first-two-thirds",  # Left Two Thirds
    "r": "center-two-thirds",  # Center Two Thirds
    "t": "last-two-thirds",  # Right Two Thirds
    # Display management (y/o for left/right display)
    "o": "next-desktop",  # Next Display
    "y": "previous-desktop",  # Previous Display
    # Special actions
    "spacebar": "almost-maximize",  # Maximize
    "return_or_enter": "maximize",  # Maximize
    "c": "center",  # Center
    "delete_or_backspace": "restore",  # Restore
}


def create_config():
    # Example configuration similar to the provided TypeScript code
    config = {
        # b = "Browse"
        "b": {
            "x": open_url("https://twitter.com"),
            "g": open_url("https://github.com"),
            "o": open_url("https://stackoverflow.com"),
            "r": open_url("https://reddit.com"),
            "y": open_url("https://news.ycombinator.com"),
            "m": open_url("https://mail.google.com"),
            "t": open_url("https://app.tuta.com/mail"),
            "s": open_url("https://bsky.app"),
            "f": open_url("https://fedica.com/dash"),
            "i": open_url("https://inoreader.com/all_articles"),
        },
        # o = "Open" applications
        "o": {
            "a": "Arc",
            "b": BROWSER_APP,
            "c": "Visual Studio Code",  # Code
            "d": "Docker",
            "e": "Zed",  # Editor
            "f": "Finder",
            "m": "Mail",
            "n": "Notes",
            "r": "RStudio",  # R
            "p": "Spotify",  # Play Music
            "s": "Safari",
            "t": TERMINAL_APP,
            "v": "Positron",
            "w": "WhatsApp",
            "x": "Zotero",
            "z": "Zen",
        },
        # w = "Window" management
        "w": window_mgt_config(WINDOW_ACTIONS),
        # r = "Raycast"
        "r": {
            "a": open_url("raycast://extensions/raycast/raycast-ai/ai-chat"),
            "c": open_url("raycast://extensions/thomas/color-picker/pick-color"),
            "d": open_url("raycast://extensions/raycast/dictionary/define-word"),
            "e": open_url(
                "raycast://extensions/raycast/emoji-symbols/search-emoji-symbols"
            ),  # emoji
            "f": open_url(
                "raycast://extensions/raycast/file-search/search-files"
            ),  # find
            "l": open_url("com.apple.Lock-Screen-Settings.extension"),
            "m": open_url("raycast://extensions/raycast/system/toggle-mute"),
            "p": open_url("raycast://extensions/raycast/raycast/confetti"),  # party
            "s": open_url("raycast://extensions/raycast/snippets/search-snippets"),
            "t": open_url("raycast://extensions/gebeto/translate/translate"),
            "h": open_url(
                "raycast://extensions/raycast/clipboard-history/clipboard-history"
            ),  # history
            "v": open_url(
                "raycast://extensions/raycast/clipboard-history/clipboard-history"
            ),  # paste (e.g., in Pastebot we use cmd + shft + v)
        },
        # v = "moVe" (vim-style navigation)
        "v": {
            "h": {"to": [{"key_code": "left_arrow"}]},
            "j": {"to": [{"key_code": "down_arrow"}]},
            "k": {"to": [{"key_code": "up_arrow"}]},
            "l": {"to": [{"key_code": "right_arrow"}]},
            "u": {"to": [{"key_code": "page_up"}]},
            "d": {"to": [{"key_code": "page_down"}]},
        },
        # s = "System"
        "s": {
            "u": {"to": [{"key_code": "volume_increment"}]},
            "j": {"to": [{"key_code": "volume_decrement"}]},
            "i": {"to": [{"key_code": "display_brightness_increment"}]},
            "k": {"to": [{"key_code": "display_brightness_decrement"}]},
            "p": {"to": [{"key_code": "play_or_pause"}]},
        },
    }

    kb = KarabinerConfig()
    kb.create_config_from_dict(config)
    kb.save_config()


if __name__ == "__main__":
    create_config()
