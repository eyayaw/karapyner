import json
from typing import Any

from utils import app, open_url


class KarabinerConfig:
    def __init__(self):
        self.rules: list[dict] = []
        self.sublayers: dict[str, dict[str, Any]] = {}

    def _create_hyper_key_rule(self) -> dict:
        """Create the hyper key (caps_lock) configuration"""
        return {
            "description": "Hyper Key (⌃⌥⇧⌘)",
            "manipulators": [
                {
                    "description": "Caps Lock -> Hyper Key",
                    "from": {
                        "key_code": "caps_lock",
                        "modifiers": {"optional": ["any"]},
                    },
                    "to": [{"set_variable": {"name": "hyper", "value": 1}}],
                    "to_after_key_up": [
                        {"set_variable": {"name": "hyper", "value": 0}}
                    ],
                    "to_if_alone": [{"key_code": "escape"}],
                    "type": "basic",
                }
            ],
        }

    # shift double press for caps lock
    def _create_double_press_caps_lock_rule(self) -> dict:
        return {
            "description": "Change double press of left-shift to caps lock",
            "manipulators": [
                {
                    "conditions": [
                        {
                            "name": "left_shift pressed",
                            "type": "variable_if",
                            "value": 1,
                        }
                    ],
                    "from": {
                        "key_code": "left_shift",
                        "modifiers": {"optional": ["any"]},
                    },
                    "to": [{"key_code": "caps_lock"}],
                    "type": "basic",
                },
                {
                    "from": {
                        "key_code": "left_shift",
                        "modifiers": {"optional": ["any"]},
                    },
                    "to": [
                        {"set_variable": {"name": "left_shift pressed", "value": 1}},
                        {"key_code": "left_shift"},
                    ],
                    "to_delayed_action": {
                        "to_if_canceled": [
                            {"set_variable": {"name": "left_shift pressed", "value": 0}}
                        ],
                        "to_if_invoked": [
                            {"set_variable": {"name": "left_shift pressed", "value": 0}}
                        ],
                    },
                    "type": "basic",
                },
            ],
        }

    def _create_sublayer_bindings(
        self, layer_key: str, bindings: dict[str, Any]
    ) -> list[dict]:
        """Create bindings for a sublayer"""

        # Create a single rule for the sublayer with all manipulators
        rule = {"description": f'Hyper Key sublayer "{layer_key}"', "manipulators": []}

        # Add the sublayer activation manipulator
        rule["manipulators"].append(
            {
                "type": "basic",
                "conditions": [{"name": "hyper", "type": "variable_if", "value": 1}],
                "description": f"Toggle Hyper sublayer {layer_key}",
                "from": {"key_code": layer_key, "modifiers": {"optional": ["any"]}},
                "to": [
                    {
                        "set_variable": {
                            "name": f"hyper_sublayer_{layer_key}",
                            "value": 1,
                        }
                    }
                ],
                "to_after_key_up": [
                    {
                        "set_variable": {
                            "name": f"hyper_sublayer_{layer_key}",
                            "value": 0,
                        }
                    }
                ],
            }
        )

        # Add individual key binding manipulators
        for key, action in bindings.items():
            if isinstance(action, str):
                # Handle string shortcuts
                if action.startswith("http"):
                    action = open_url(action)
                else:
                    action = app(action)

            manipulator = {
                "type": "basic",
                "conditions": [
                    {
                        "name": f"hyper_sublayer_{layer_key}",
                        "type": "variable_if",
                        "value": 1,
                    }
                ],
                "from": {"key_code": key, "modifiers": {"optional": ["any"]}},
            }

            if isinstance(action, dict):
                if "to" in action:
                    manipulator["to"] = action["to"]
                else:
                    manipulator["to"] = [{"shell_command": f"open -a '{action}.app'"}]
                if "description" in action:
                    manipulator["description"] = action["description"]

            rule["manipulators"].append(manipulator)

        return [rule]

    def create_config_from_dict(self, config: dict[str, dict[str, Any]]) -> None:
        """Create configuration from a dictionary of sublayers"""
        # Add the hyper key rule
        self.rules.append(self._create_hyper_key_rule())

        # Add the double press caps lock rule
        self.rules.append(self._create_double_press_caps_lock_rule())

        # Process each sublayer
        for layer_key, bindings in config.items():
            self.rules.extend(self._create_sublayer_bindings(layer_key, bindings))

    def _other_configs(self):
        return {
            "devices": [
                {
                    "identifiers": {
                        "is_keyboard": True,
                        "is_pointing_device": True,
                        "product_id": 45915,
                        "vendor_id": 1133,
                    },
                    "ignore": False,
                }
            ],
            "virtual_hid_keyboard": {
                "country_code": 0,
                "keyboard_type_v2": "ansi",
            },
        }

    def save_config(self, filepath: str = "karabiner.json") -> None:
        """Save the configuration to a Karabiner-Elements JSON file"""
        config = {
            "global": {"show_in_menu_bar": False},
            "profiles": [
                {
                    "name": "Default",
                    "complex_modifications": {
                        "parameters": {
                            "basic.simultaneous_threshold_milliseconds": 50,
                            "basic.to_delayed_action_delay_milliseconds": 500,
                            "basic.to_if_alone_timeout_milliseconds": 1000,
                            "basic.to_if_held_down_threshold_milliseconds": 500,
                        },
                        "rules": self.rules,
                    },
                    **self._other_configs(),
                }
            ],
        }

        with open(filepath, "w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
