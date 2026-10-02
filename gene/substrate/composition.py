"""Compositional operations for constructing unseen structured states."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Composition:
    parts: tuple[Any, ...]
    attributes: tuple[tuple[str, Any], ...] = ()

    def with_attribute(self, name: str, value: Any) -> "Composition":
        attrs = dict(self.attributes)
        attrs[name] = value
        return Composition(self.parts, tuple(attrs.items()))


def compose(*parts: Any, **attributes: Any) -> Composition:
    return Composition(tuple(parts), tuple(attributes.items()))
