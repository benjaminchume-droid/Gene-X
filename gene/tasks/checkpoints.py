"""Serializable task checkpoints for pause, recovery, and continuation."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class Checkpoint:
    task_id: str
    state: Any
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)

class CheckpointStore:
    def __init__(self) -> None:
        self._checkpoints: dict[str, Checkpoint] = {}

    def save(self, checkpoint: Checkpoint) -> None:
        self._checkpoints[checkpoint.task_id] = checkpoint

    def load(self, task_id: str) -> Checkpoint | None:
        return self._checkpoints.get(task_id)

    def delete(self, task_id: str) -> None:
        self._checkpoints.pop(task_id, None)
