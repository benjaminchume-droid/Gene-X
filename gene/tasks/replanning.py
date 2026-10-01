"""Explicit replanning boundary for failed or blocked work."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(slots=True)
class ReplanResult:
    changed: bool
    reason: str
    replacement: Any = None

class Replanner:
    def __init__(self, strategy: Callable[[Any, Exception | None], Any]) -> None:
        self.strategy = strategy

    def replan(self, state: Any, error: Exception | None = None) -> ReplanResult:
        replacement = self.strategy(state, error)
        return ReplanResult(changed=replacement is not None, reason="strategy evaluated", replacement=replacement)
