"""Bridge from durable objectives to mutable execution work graphs."""
from __future__ import annotations

from dataclasses import dataclass

from .model import Objective
from gene.brain.long_task import LongTaskController, WorkItem


@dataclass
class ObjectiveRuntime:
    objective: Objective
    controller: LongTaskController

    @classmethod
    def create(cls, objective: Objective) -> "ObjectiveRuntime":
        return cls(objective, LongTaskController(objective.objective_id))

    def add_plan_step(self, description: str, *, dependencies: set[str] | None = None) -> WorkItem:
        return self.controller.add_work(description, dependencies=dependencies)

    def amend_plan(self, description: str, *, dependencies: set[str] | None = None) -> WorkItem:
        return self.controller.amend(description, dependencies=dependencies)
