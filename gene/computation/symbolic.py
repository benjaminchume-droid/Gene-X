"""Symbolic transformation boundary for exact computation."""
from __future__ import annotations
from typing import Any, Callable

class SymbolicSystem:
    def __init__(self) -> None:
        self._rules: list[Callable[[Any], Any]] = []

    def add_rule(self, rule: Callable[[Any], Any]) -> None:
        self._rules.append(rule)

    def transform(self, value: Any) -> Any:
        result = value
        for rule in self._rules:
            result = rule(result)
        return result
