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
    def __init__(self): self.values = {}
    def set(self, name, value, source=None): self.values[name] = Property(name, value, source)
    def get(self, name, default=None):
        item = self.values.get(name)
        return default if item is None else item.value
