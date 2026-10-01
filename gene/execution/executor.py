"""Generic execution primitive with optional retry and recovery."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class ExecutionResult:
    value: Any = None
    error: Exception | None = None
    attempts: int = 0

class Executor:
    def execute(self, operation: Callable[[], Any], *, retries: int = 0,
                recover: Callable[[Exception, int], Any] | None = None) -> ExecutionResult:
        if retries < 0:
            raise ValueError("retries cannot be negative")
        for attempt in range(1, retries + 2):
            try:
                return ExecutionResult(value=operation(), attempts=attempt)
            except Exception as exc:
                if recover is not None:
                    recovered = recover(exc, attempt)
                    if recovered is not None:
                        return ExecutionResult(value=recovered, attempts=attempt)
                if attempt > retries:
                    return ExecutionResult(error=exc, attempts=attempt)
        raise RuntimeError("unreachable")
