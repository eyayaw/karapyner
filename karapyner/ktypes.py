from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, TypedDict, Union


class Sublayer(Enum):
    BROWSE = "browse"
    OPEN = "open"
    WINDOW = "window"
    RAYCAST = "raycast"
    MOVE = "move"
    SYSTEM = "system"


class KeyCode(Enum):
    LEFT_ARROW = "left_arrow"
    RIGHT_ARROW = "right_arrow"
    UP_ARROW = "up_arrow"
    DOWN_ARROW = "down_arrow"
    PAGE_UP = "page_up"
    PAGE_DOWN = "page_down"
    CAPS_LOCK = "caps_lock"
    ESCAPE = "escape"
    RETURN = "return_or_enter"
    SPACEBAR = "spacebar"


@dataclass
class Binding:
    key: str
    action: Union[str, dict[str, Any]]
    description: Optional[str] = None


class Manipulator(TypedDict):
    type: str
    description: Optional[str]
    from_: dict[str, Any]
    to: list[dict[str, Any]]
    conditions: Optional[list[dict[str, Any]]]


class Rule(TypedDict):
    description: str
    manipulators: list[Manipulator]


@dataclass
class KarabinerRule:
    description: str
    manipulators: list[Manipulator]
