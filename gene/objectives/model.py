"""Persistent objective state and explicit amendment semantics."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from gene.tasks.priorities import Priority


class ObjectiveStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class ObjectiveChange:
    """A change request that augments or constrains an existing objective."""

    description: str
    additions: tuple[str, ...] = ()
    constraints: tuple[str, ...] = ()
    removals: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Objective:
    """A durable goal independent of any particular execution plan."""

    description: str
    objective_id: str = field(default_factory=lambda: str(uuid4()))
    status: ObjectiveStatus = ObjectiveStatus.ACTIVE
    priority: Priority = field(default_factory=Priority)
    parent_id: str | None = None
    dependencies: set[str] = field(default_factory=set)
    additions: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    version: int = 0

    def amend(self, change: ObjectiveChange) -> int:
        """Apply an additive change without replacing the existing objective."""
        if self.status in {ObjectiveStatus.COMPLETED, ObjectiveStatus.CANCELLED}:
            raise ValueError(f"cannot amend {self.status.value} objective")
        self.additions.extend(change.additions)
        self.constraints.extend(change.constraints)
        if change.removals:
            removal_set = set(change.removals)
            self.additions[:] = [item for item in self.additions if item not in removal_set]
            self.constraints[:] = [item for item in self.constraints if item not in removal_set]
        self.metadata.update(change.metadata)
        self.version += 1
        return self.version

    def cancel(self) -> None:
        if self.status != ObjectiveStatus.COMPLETED:
            self.status = ObjectiveStatus.CANCELLED

    def pause(self) -> None:
        if self.status == ObjectiveStatus.ACTIVE:
            self.status = ObjectiveStatus.PAUSED

    def resume(self) -> None:
        if self.status == ObjectiveStatus.PAUSED:
            self.status = ObjectiveStatus.ACTIVE
