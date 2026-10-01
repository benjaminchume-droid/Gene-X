"""Recovery policy primitives for failed or stalled work."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class RecoveryAction:
    name: str
    execute: Callable[[Exception], Any]

class RecoveryPolicy:
    def __init__(self, actions: list[RecoveryAction] | None = None) -> None:
        self.actions = actions or []

    def recover(self, error: Exception) -> Any:
        last_error = error
        for action in self.actions:
            try:
                return action.execute(error)
            except Exception as exc:
                last_error = exc
        raise last_error
