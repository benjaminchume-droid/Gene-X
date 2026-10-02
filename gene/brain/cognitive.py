"""High-level bridge between learned prediction and explicit cognition."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .context import ContextStore
from .model import BrainOutput, GeneBrain
from .representation import StructuredExample
from .long_task import LongTaskController


@dataclass
class CognitiveState:
    """Current working state; persistent memory remains outside this object."""

    observation: Any = None
    interpretation: Any = None
    decision: Any = None
    active_objective: str | None = None


class CognitiveSystem:
    """Hybrid entry point.

    The neural component proposes learned interpretations. Explicit structures
    retain entities, state, objectives, work graphs and exact operations. This
    prevents the learned component from becoming the sole source of truth.
    """

    def __init__(self, brain: GeneBrain | None = None) -> None:
        self.brain = brain or GeneBrain()
        self.context = ContextStore()
        self.state = CognitiveState()
        self.objectives: dict[str, LongTaskController] = {}

    def observe(self, observation: Any, *, bucket: str = "observation") -> None:
        self.state.observation = observation
        self.context.add(bucket, observation, priority=1.0)

    def interpret(self, structure: StructuredExample) -> BrainOutput:
        result = self.brain.predict(structure)
        self.state.interpretation = result
        self.context.add("interpretation", result, priority=2.0)
        return result

    def start_objective(self, objective_id: str) -> LongTaskController:
        controller = LongTaskController(objective_id)
        self.objectives[objective_id] = controller
        self.state.active_objective = objective_id
        return controller

    def objective(self, objective_id: str) -> LongTaskController:
        return self.objectives[objective_id]
