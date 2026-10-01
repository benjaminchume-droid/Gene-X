"""Process lifecycle records for executable work."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class ProcessStatus(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    EXITED = "exited"
    FAILED = "failed"
    TERMINATED = "terminated"

@dataclass
class ProcessRecord:
    process_id: str
    status: ProcessStatus = ProcessStatus.CREATED
    return_code: int | None = None
    error: str | None = None

    def transition(self, status: ProcessStatus) -> None:
        self.status = status
