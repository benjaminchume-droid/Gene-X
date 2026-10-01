"""Reusable transformations over world state."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(slots=True)
class Transformation:
    name: str
    apply: Callable[[Any], Any]
    reversible: bool = False

    def __call__(self, value: Any) -> Any:
        return self.apply(value)
