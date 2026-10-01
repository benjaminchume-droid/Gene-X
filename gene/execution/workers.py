"""Worker execution with explicit lifecycle and failure capture."""
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

    def run(self, operation: Callable[[], Any]) -> WorkerResult:
        self.status = WorkerStatus.RUNNING
        try:
            value = operation()
            self.status = WorkerStatus.SUCCEEDED
            return WorkerResult(self.worker_id, self.status, value=value)
        except Exception as exc:
            self.status = WorkerStatus.FAILED
            return WorkerResult(self.worker_id, self.status, error=exc)

    def stop(self) -> None:
        self.status = WorkerStatus.STOPPED
