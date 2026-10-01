"""Lifecycle and dependency management for multiple simultaneous objectives."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .conflicts import Conflict, ConflictDetector
from .model import Objective, ObjectiveChange, ObjectiveStatus


@dataclass(slots=True)
class ObjectiveManager:
    """Owns objectives without deciding how their work is executed."""

    detector: ConflictDetector = field(default_factory=ConflictDetector)
    objectives: dict[str, Objective] = field(default_factory=dict)

    def create(
        self,
        description: str,
        *,
        parent_id: str | None = None,
        dependencies: Iterable[str] = (),
        **metadata: object,
    ) -> Objective:
        if parent_id is not None and parent_id not in self.objectives:
            raise KeyError(f"unknown parent objective: {parent_id}")
        dependency_ids = set(dependencies)
        missing = dependency_ids - self.objectives.keys()
        if missing:
            raise KeyError(f"unknown objective dependencies: {sorted(missing)}")
        objective = Objective(
            description=description,
            parent_id=parent_id,
            dependencies=dependency_ids,
            metadata=dict(metadata),
        )
        if objective.objective_id in self.objectives:
            raise RuntimeError("objective id collision")
        self.objectives[objective.objective_id] = objective
        return objective

    def get(self, objective_id: str) -> Objective:
        return self.objectives[objective_id]

    def amend(self, objective_id: str, change: ObjectiveChange) -> Objective:
        objective = self.get(objective_id)
        objective.amend(change)
        return objective

    def cancel(self, objective_id: str, *, include_descendants: bool = False) -> tuple[str, ...]:
        """Cancel one objective, optionally cascading only through explicit parent links."""
        target = self.get(objective_id)
        cancelled: list[str] = []
        if include_descendants:
            pending = [objective_id]
            while pending:
                current = pending.pop()
                obj = self.get(current)
                if obj.status not in {ObjectiveStatus.COMPLETED, ObjectiveStatus.CANCELLED}:
                    obj.cancel()
                    cancelled.append(current)
                pending.extend(
                    child.objective_id
                    for child in self.objectives.values()
                    if child.parent_id == current
                )
        else:
            target.cancel()
            cancelled.append(objective_id)
        return tuple(cancelled)

    def pause(self, objective_id: str) -> Objective:
        objective = self.get(objective_id)
        objective.pause()
        return objective

    def resume(self, objective_id: str) -> Objective:
        objective = self.get(objective_id)
        objective.resume()
        return objective

    def dependencies_satisfied(self, objective_id: str) -> bool:
        objective = self.get(objective_id)
        return all(
            self.get(dep).status == ObjectiveStatus.COMPLETED
            for dep in objective.dependencies
        )

    def ready(self) -> tuple[Objective, ...]:
        return tuple(
            objective
            for objective in self.objectives.values()
            if objective.status == ObjectiveStatus.ACTIVE and self.dependencies_satisfied(objective.objective_id)
        )

    def conflicts(self) -> tuple[Conflict, ...]:
        return self.detector.detect(self.objectives.values())

    def active(self) -> tuple[Objective, ...]:
        return tuple(o for o in self.objectives.values() if o.status == ObjectiveStatus.ACTIVE)
