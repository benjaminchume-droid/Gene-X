"""Properties are first-class values attached to world entities."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class Property:
    name: str
    value: Any
    source: str | None = None

@dataclass(slots=True)
class PropertySet:
    values: dict[str, Property]

    def __init__(self) -> None:
        self.values = {}

    def set(self, name: str, value: Any, source: str | None = None) -> None:
        self.values[name] = Property(name, value, source)

    def get(self, name: str, default: Any = None) -> Any:
        item = self.values.get(name)
        return default if item is None else item.value
