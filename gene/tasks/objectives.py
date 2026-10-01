"""Persistent objectives that can own and evolve task graphs."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

class ObjectiveStatus(StrEnum):
    ACTIVE="active"
    PAUSED="paused"
    COMPLETED="completed"
    FAILED="failed"
    CANCELLED="cancelled"

@dataclass
class Objective:
    description: str
    objective_id: str = field(default_factory=lambda: str(uuid4()))
    status: ObjectiveStatus = ObjectiveStatus.ACTIVE
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def set_status(self, status: ObjectiveStatus) -> None:
        self.status = status
        self.updated_at = datetime.now(timezone.utc)
