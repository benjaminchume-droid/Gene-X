"""Worker execution with lifecycle, cancellation, and failure capture."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable
from uuid import uuid4

class WorkerStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    STOPPED = "stopped"

@dataclass
class WorkerResult:
    worker_id: str
    status: WorkerStatus
    value: Any = None
    error: Exception | None = None

class Worker:
    def __init__(self, name: str) -> None:
        self.name = name
        self.worker_id = uuid4().hex
        self.status = WorkerStatus.IDLE
        self._stop_requested = False

    def run(self, operation: Callable[[], Any]) -> WorkerResult:
        if self.status == WorkerStatus.RUNNING:
            raise RuntimeError("worker is already running")
        self._stop_requested = False
        self.status = WorkerStatus.RUNNING
        try:
            value = operation()
            if self._stop_requested:
                self.status = WorkerStatus.STOPPED
                return WorkerResult(self.worker_id, self.status, value=value)
            self.status = WorkerStatus.SUCCEEDED
            return WorkerResult(self.worker_id, self.status, value=value)
        except Exception as exc:
            self.status = WorkerStatus.STOPPED if self._stop_requested else WorkerStatus.FAILED
            return WorkerResult(self.worker_id, self.status, error=exc)

    def request_stop(self) -> None:
        self._stop_requested = True

    def stop(self) -> None:
        self.request_stop()
        if self.status != WorkerStatus.RUNNING:
            self.status = WorkerStatus.STOPPED
