"""Continuous cognition and learning cycle.

The cycle is an orchestration primitive, not a hard-coded task solver. It
accepts observations, objectives, actions, verification and learning signals
as data or callbacks and feeds the resulting experience back into the system.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

from gene.memory.episodic import EpisodicMemory
from gene.memory.procedural import ProceduralMemory
from gene.memory.semantic import SemanticMemory
from gene.memory.working import WorkingMemory
from gene.memory.store import MemoryStore, MemoryRecord
from gene.objectives.manager import ObjectiveManager
from gene.objectives.model import Objective
from gene.substrate.state import StateStore
from gene.substrate.ontology import WorldModel
from gene.brain.representation import StructuredExample
from gene.brain.model import GeneBrain, BrainOutput


@dataclass(frozen=True)
class CycleObservation:
    value: Any
    structure: StructuredExample
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CycleAction:
    name: str
    payload: Any = None


@dataclass(frozen=True)
class CycleEvaluation:
    passed: bool
    score: float
    feedback: Any = None


@dataclass(frozen=True)
class CycleResult:
    observation: CycleObservation
    interpretation: Any
    action: CycleAction | None
    execution: Any
    evaluation: CycleEvaluation | None
    learned: bool
    objective_id: str | None


class CognitionCycle:
    """One reusable observe -> understand -> decide -> act -> verify -> learn cycle."""

    def __init__(
        self,
        *,
        brain: GeneBrain | None = None,
        state: StateStore | None = None,
        world: WorldModel | None = None,
        objectives: ObjectiveManager | None = None,
        working: WorkingMemory | None = None,
        episodic: EpisodicMemory | None = None,
        semantic: SemanticMemory | None = None,
        procedural: ProceduralMemory | None = None,
        memory: MemoryStore | None = None,
    ) -> None:
        self.brain = brain or GeneBrain()
        self.state = state or StateStore()
        self.world = world or WorldModel()
        self.objectives = objectives or ObjectiveManager()
        self.working = working or WorkingMemory()
        self.episodic = episodic or EpisodicMemory()
        self.semantic = semantic or SemanticMemory()
        self.procedural = procedural or ProceduralMemory()
        self.memory = memory or MemoryStore()
        self.step_count = 0

    def _remember(self, observation: CycleObservation) -> None:
        self.working.add(observation)
        self.episodic.record(observation.value, **observation.metadata)
        self.memory.put(
            MemoryRecord(
                key=f"cycle:{self.step_count}",
                value=observation.value,
                kind="experience",
                metadata=observation.metadata,
            )
        )
        self.state.set("last_observation", observation.value, source="cognition-cycle")

    def step(
        self,
        observation: CycleObservation,
        *,
        objective: Objective | None = None,
        action_selector: Callable[[Any, Objective | None, tuple[Any, ...]], CycleAction | None] | None = None,
        executor: Callable[[CycleAction], Any] | None = None,
        evaluator: Callable[[CycleAction, Any, CycleObservation], CycleEvaluation] | None = None,
        learning: bool = True,
        representation_training: bool = True,
    ) -> CycleResult:
        self.step_count += 1
        self._remember(observation)

        interpretation: Any
        if self.brain.labels:
            interpretation = self.brain.predict(observation.structure)
        else:
            interpretation = self.brain.representation.encode(observation.structure)

        self.state.set("last_interpretation", interpretation, source="cognition-cycle")
        self.working.add(interpretation)

        recalled = tuple(self.episodic.recent(limit=8))
        action = action_selector(interpretation, objective, recalled) if action_selector else None

        execution = None
        evaluation = None
        if action is not None and executor is not None:
            execution = executor(action)
            if evaluator is not None:
                evaluation = evaluator(action, execution, observation)

        learned = False
        if learning and representation_training:
            report = self.brain.train_representation([observation.structure], epochs=1)
            learned = report.steps > 0
            self.state.set("last_learning_report", report, source="cognition-cycle")

        self.episodic.record(
            {"action": action, "execution": execution, "evaluation": evaluation},
            objective_id=objective.objective_id if objective else None,
        )
        if evaluation is not None:
            self.semantic.set(
                f"cycle:{self.step_count}:evaluation",
                evaluation,
            )

        return CycleResult(
            observation=observation,
            interpretation=interpretation,
            action=action,
            execution=execution,
            evaluation=evaluation,
            learned=learned,
            objective_id=objective.objective_id if objective else None,
        )

    def run(
        self,
        observations: Iterable[CycleObservation],
        **kwargs: Any,
    ) -> tuple[CycleResult, ...]:
        return tuple(self.step(item, **kwargs) for item in observations)
