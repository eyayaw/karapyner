import json
import logging
from pathlib import Path
from typing import Any

from config.paths import KARABINER_CONFIG_PATH
from karapyner.builders import ConfigurationError, ManipulatorBuilder, RuleBuilder
from karapyner.ktypes import KeyCode, Manipulator, Rule, Sublayer
from karapyner.utils import open_app, open_url, open_raycast_deeplink

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class KarabinerConfig:
    def __init__(self):
        self.rules: list[Rule] = []
        self.sublayers: dict[Sublayer, dict[str, Any]] = {}
        self.sublayer_keys: dict[str, str] = {}

    def _create_hyper_key_rule(self) -> Rule:
        """Create the hyper key (caps_lock) configuration"""
        try:
            manipulator = (
                ManipulatorBuilder()
                .with_description("Caps Lock -> Hyper Key")
                .with_from_key_code(KeyCode.CAPS_LOCK, modifiers={"optional": ["any"]})
                .with_to([{"set_variable": {"name": "hyper", "value": 1}}])
                .with_to_after_key_up([{"set_variable": {"name": "hyper", "value": 0}}])
                .with_to_if_alone([{"key_code": KeyCode.ESCAPE.value}])
                .build()
            )

            rule = (
                RuleBuilder()
                .with_description("Hyper Key (⌃⌥⇧⌘)")
                .with_manipulator(manipulator)
                .build()
            )

            return rule
        except ConfigurationError as e:
            logger.error(f"Failed to create hyper key rule: {e}")
            raise

    def _create_caps_lock_rule(self) -> Rule:
        """Create the double press shift for caps lock rule"""
        try:
            # First manipulator: handles the double press
            first_manipulator = (
                ManipulatorBuilder()
                .with_from_key_code("left_shift", modifiers={"optional": ["any"]})
                .with_condition(
                    {
                        "name": "left_shift pressed",
                        "type": "variable_if",
                        "value": 1,
                    }
                )
                .with_to([{"key_code": "caps_lock"}])
                .build()
            )

            # Second manipulator: handles the first press
            second_manipulator = (
                ManipulatorBuilder()
                .with_from_key_code("left_shift", modifiers={"optional": ["any"]})
                .with_to(
                    [
                        {"set_variable": {"name": "left_shift pressed", "value": 1}},
                        {"key_code": "left_shift"},
                    ]
                )
                .with_to_delayed_action(
                    {
                        "to_if_canceled": [
                            {"set_variable": {"name": "left_shift pressed", "value": 0}}
                        ],
                        "to_if_invoked": [
                            {"set_variable": {"name": "left_shift pressed", "value": 0}}
                        ],
                    }
                )
                .build()
            )

            rule = (
                RuleBuilder()
                .with_description("Change double press of left-shift to caps lock")
                .with_manipulator(first_manipulator)
                .with_manipulator(second_manipulator)
                .build()
            )

            return rule
        except ConfigurationError as e:
            logger.error(f"Failed to create double press caps lock rule: {e}")
            raise

    def _create_sublayer_bindings(
        self, layer: Sublayer, bindings: dict[str, Any]
    ) -> list[Rule]:
        """Create bindings for a sublayer"""
        try:
            rule_builder = RuleBuilder().with_description(
                f"Hyper Key sublayer '{self.sublayer_keys[layer.value]}'"
            )

            # Add activation manipulator
            activation_manipulator = self._create_activation_manipulator(layer)
            rule_builder.with_manipulator(activation_manipulator)

            # Add key bindings
            for key, action in bindings.items():
                manipulator = self._create_key_manipulator(layer, key, action)
                rule_builder.with_manipulator(manipulator)

            return [rule_builder.build()]
        except ConfigurationError as e:
            logger.error(f"Failed to create sublayer bindings for '{layer.value}': {e}")
            raise

    def create_config_from_dict(self, config: dict[str, dict[str, Any]]) -> None:
        """Create configuration from a dictionary of sublayers"""
        try:
            # Extract and store sublayer key mappings
            self.sublayer_keys = config.pop("sublayer_keys", {})
            if not self.sublayer_keys:
                raise ConfigurationError("sublayer_keys configuration is required")

            # Validate config
            self._validate_config(config)

            # Add the hyper key rule
            self.rules.append(self._create_hyper_key_rule())

            # Add the double press caps lock rule
            self.rules.append(self._create_caps_lock_rule())

            # Process each sublayer
            for layer_key, bindings in config.items():
                try:
                    layer = Sublayer(layer_key)
                    self.rules.extend(self._create_sublayer_bindings(layer, bindings))
                except ValueError:
                    logger.warning(f"Invalid sublayer key: '{layer_key}', skipping...")
                    continue

        except Exception as e:
            logger.error(f"Failed to create configuration: {e}")
            raise

    def _create_activation_manipulator(self, layer: Sublayer) -> Manipulator:
        """Create the activation manipulator for a sublayer"""
        sublayer_key = self.sublayer_keys[layer.value]
        return (
            ManipulatorBuilder()
            .with_description(f"Toggle Hyper sublayer {sublayer_key}")
            .with_from_key_code(sublayer_key, modifiers={"optional": ["any"]})
            .with_condition({"name": "hyper", "type": "variable_if", "value": 1})
            .with_to(
                [
                    {
                        "set_variable": {
                            "name": f"hyper_sublayer_{sublayer_key}",
                            "value": 1,
                        }
                    }
                ]
            )
            .with_to_after_key_up(
                [
                    {
                        "set_variable": {
                            "name": f"hyper_sublayer_{sublayer_key}",
                            "value": 0,
                        }
                    }
                ]
            )
            .build()
        )

    def _create_key_manipulator(
        self, layer: Sublayer, key: str, action: str | dict[str, Any]
    ) -> Manipulator:
        """Create a key manipulator for a specific binding"""
        sublayer_key = self.sublayer_keys[layer.value]

        # Process the action
        if isinstance(action, str):
            if "https://" in action:
                action = open_url(action)
            elif "raycast://" in action:
                action = open_raycast_deeplink(action)
            # TODO: add a robust way to handle app names (append .app in the config?)
            else:
                action = open_app(action)

        manipulator = (
            ManipulatorBuilder()
            .with_from_key_code(key, modifiers={"optional": ["any"]})
            .with_condition(
                {
                    "name": f"hyper_sublayer_{sublayer_key}",
                    "type": "variable_if",
                    "value": 1,
                }
            )
        )

        if isinstance(action, dict):
            if "to" in action:
                manipulator.with_to(action["to"])
            else:
                manipulator.with_to(open_app(action)["to"])
            if "description" in action:
                manipulator.with_description(action["description"])

        return manipulator.build()

    def _other_configs(self) -> dict[str, Any]:
        """Additional Karabiner configuration settings"""
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

    def _validate_config(self, config: dict[str, dict[str, Any]]) -> None:
        """Validate the configuration dictionary"""
        if not config:
            raise ConfigurationError("Configuration cannot be empty")

        for layer_key, bindings in config.items():
            if not isinstance(bindings, dict):
                raise ConfigurationError(
                    f"Bindings for layer '{layer_key}' must be a dictionary"
                )
            if not bindings:
                raise ConfigurationError(
                    f"Bindings for layer '{layer_key}' cannot be empty"
                )

    def save_config(self, filepath: str = KARABINER_CONFIG_PATH) -> None:
        """Save the configuration to a Karabiner-Elements JSON file"""
        try:
            config = self._create_full_config()

            # Ensure the directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, "w") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                logger.info(f"Configuration successfully saved to {filepath}")

        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise

    def _create_full_config(self) -> dict[str, Any]:
        """Create the full configuration dictionary"""
        return {
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
