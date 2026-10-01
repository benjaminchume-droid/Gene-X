"""Control loop for persistent objectives and recoverable execution."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any

from ..tasks.objectives import Objective, ObjectiveStatus
from ..tasks.objective_store import ObjectiveStore
from ..tasks.replanning import Replanner, ReplanResult
from ..tasks.checkpoints import Checkpoint, CheckpointStore
from .events import Event, EventBus

@dataclass
class AutonomyController:
    objectives: ObjectiveStore = field(default_factory=ObjectiveStore)
    checkpoints: CheckpointStore = field(default_factory=CheckpointStore)
    events: EventBus = field(default_factory=EventBus)
    replanners: dict[str, Replanner] = field(default_factory=dict)

    def register(self, objective: Objective, replanner: Replanner | None = None) -> None:
        self.objectives.save(objective)
        if replanner is not None:
            self.replanners[objective.objective_id] = replanner
        self.events.publish(Event("objective.registered", {"objective_id": objective.objective_id}))

    def checkpoint(self, objective_id: str, state: Any, metadata: dict[str, Any] | None = None) -> None:
        self.checkpoints.save(Checkpoint(objective_id, state, metadata=metadata or {}))
        self.events.publish(Event("objective.checkpointed", {"objective_id": objective_id}))

    def pause(self, objective_id: str) -> None:
        objective = self._require(objective_id)
        objective.set_status(ObjectiveStatus.PAUSED)
        self.events.publish(Event("objective.paused", {"objective_id": objective_id}))

    def resume(self, objective_id: str) -> Checkpoint | None:
        objective = self._require(objective_id)
        objective.set_status(ObjectiveStatus.ACTIVE)
        checkpoint = self.checkpoints.load(objective_id)
        self.events.publish(Event("objective.resumed", {"objective_id": objective_id, "has_checkpoint": checkpoint is not None}))
        return checkpoint

    def recover(self, objective_id: str, error: Exception | None = None) -> ReplanResult | None:
        replanner = self.replanners.get(objective_id)
        if replanner is None:
            return None
        checkpoint = self.checkpoints.load(objective_id)
        state = checkpoint.state if checkpoint else None
        result = replanner.replan(state, error)
        self.events.publish(Event("objective.replanned", {"objective_id": objective_id, "changed": result.changed}))
        return result

    def complete(self, objective_id: str) -> None:
        objective = self._require(objective_id)
        objective.set_status(ObjectiveStatus.COMPLETED)
        self.events.publish(Event("objective.completed", {"objective_id": objective_id}))

    def _require(self, objective_id: str) -> Objective:
        objective = self.objectives.get(objective_id)
        if objective is None:
            raise KeyError(objective_id)
        return objective
