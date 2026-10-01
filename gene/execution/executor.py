"""Generic execution primitive for callable work."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class ExecutionResult:
    value: Any = None
    error: Exception | None = None

class Executor:
    def execute(self, operation: Callable[[], Any]) -> ExecutionResult:
        try:
            return ExecutionResult(value=operation())
        except Exception as exc:
            return ExecutionResult(error=exc)
