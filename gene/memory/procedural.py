"""Memory of executable procedures."""
from __future__ import annotations
from typing import Any, Callable

class ProceduralMemory:
    def __init__(self) -> None:
        self._procedures: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, procedure: Callable[..., Any]) -> None:
        if name in self._procedures:
            raise ValueError(f"procedure already registered: {name}")
        self._procedures[name] = procedure

    def get(self, name: str) -> Callable[..., Any]:
        return self._procedures[name]

    def names(self) -> tuple[str, ...]:
        return tuple(self._procedures)
