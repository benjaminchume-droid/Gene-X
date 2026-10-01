"""Concept/fact memory backed by explicit keys."""
from __future__ import annotations
from typing import Any

class SemanticMemory:
    def __init__(self) -> None:
        self._facts: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._facts[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._facts.get(key, default)

    def items(self) -> tuple[tuple[str, Any], ...]:
        return tuple(self._facts.items())
