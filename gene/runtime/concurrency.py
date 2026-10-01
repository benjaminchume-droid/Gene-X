"""Concurrent work coordination with explicit completion records."""
from __future__ import annotations
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Completion:
    work_id: str
    value: Any = None
    error: Exception | None = None

class ConcurrentRunner:
    def __init__(self, workers: int = 2) -> None:
        if workers < 1:
            raise ValueError("workers must be positive")
        self._executor = ThreadPoolExecutor(max_workers=workers)

    def submit(self, work_id: str, operation: Callable[[], Any]) -> Future[Completion]:
        return self._executor.submit(self._run, work_id, operation)

    @staticmethod
    def _run(work_id: str, operation: Callable[[], Any]) -> Completion:
        try:
            return Completion(work_id, value=operation())
        except Exception as exc:
            return Completion(work_id, error=exc)

    def shutdown(self, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait)
