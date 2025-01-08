from typing import Any, Optional

from karapyner.ktypes import KeyCode, Manipulator, Rule


class KarabinerError(Exception):
    """Base exception for all Karabiner-related errors"""

    pass


class ConfigurationError(KarabinerError):
    """Raised when there's an error in the configuration"""

    pass


class ValidationError(KarabinerError):
    """Raised when validation of a configuration fails"""

    pass


class ManipulatorBuilder:
    def __init__(self):
        self._manipulator: dict[str, Any] = {
            "type": "basic",
            "from": {},
            "to": [],
            "conditions": [],
        }

    def with_type(self, type_: str) -> "ManipulatorBuilder":
        self._manipulator["type"] = type_
        return self

    def with_description(self, description: str) -> "ManipulatorBuilder":
        self._manipulator["description"] = description
        return self

    def with_from_key_code(
        self, key_code: KeyCode | str, modifiers: Optional[dict] = None
    ) -> "ManipulatorBuilder":
        self._manipulator["from"] = {
            "key_code": key_code.value if isinstance(key_code, KeyCode) else key_code
        }
        if modifiers:
            self._manipulator["from"]["modifiers"] = modifiers
        return self

    def with_to(self, to_actions: list[dict[str, Any]]) -> "ManipulatorBuilder":
        self._manipulator["to"].extend(to_actions)
        return self

    def with_to_after_key_up(
        self, actions: list[dict[str, Any]]
    ) -> "ManipulatorBuilder":
        self._manipulator["to_after_key_up"] = actions
        return self

    def with_to_if_alone(self, actions: list[dict[str, Any]]) -> "ManipulatorBuilder":
        self._manipulator["to_if_alone"] = actions
        return self

    def with_to_delayed_action(self, action: dict[str, Any]) -> "ManipulatorBuilder":
        self._manipulator["to_delayed_action"] = action
        return self

    def with_condition(self, condition: dict[str, Any]) -> "ManipulatorBuilder":
        self._manipulator["conditions"].append(condition)
        return self

    def build(self) -> Manipulator:
        # Validate the manipulator before building
        if not self._manipulator["from"]:
            raise ConfigurationError("Manipulator must have 'from' key specified")
        return self._manipulator


class RuleBuilder:
    def __init__(self):
        self._rule: dict[str, Any] = {"description": "", "manipulators": []}

    def with_description(self, description: str) -> "RuleBuilder":
        self._rule["description"] = description
        return self

    def with_manipulator(self, manipulator: Manipulator) -> "RuleBuilder":
        self._rule["manipulators"].append(manipulator)
        return self

    def build(self) -> Rule:
        if not self._rule["description"]:
            raise ConfigurationError("Rule must have a description")
        if not self._rule["manipulators"]:
            raise ConfigurationError("Rule must have at least one manipulator")
        return self._rule
