"""Continuous cognition and learning cycle.

This module contains orchestration only. Domain knowledge, actions, policies,
verification, world updates, and learning targets are supplied as primitives
or callbacks rather than embedded as predetermined behavior.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Iterator

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
from gene.brain.model import GeneBrain


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
    """Observe -> represent -> retrieve -> decide -> act -> verify -> learn -> remember."""

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

    def _remember(self, observation: CycleObservation) -> tuple[Any, ...]:
        self.working.add(observation)
        recent = self.episodic.recent(limit=8)
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
        return recent

    def step(
        self,
        observation: CycleObservation,
        *,
        objective: Objective | None = None,
        action_selector: Callable[[Any, Objective | None, tuple[Any, ...]], CycleAction | None] | None = None,
        executor: Callable[[CycleAction], Any] | None = None,
        evaluator: Callable[[CycleAction, Any, CycleObservation], CycleEvaluation] | None = None,
        world_updater: Callable[[WorldModel, CycleObservation, Any, Any], Any] | None = None,
        experience_encoder: Callable[[CycleObservation, CycleAction | None, Any, CycleEvaluation | None], StructuredExample | None] | None = None,
        learning: bool = True,
    ) -> CycleResult:
        self.step_count += 1
        recent = self._remember(observation)

        if objective is None:
            ready = self.objectives.ready()
            objective = ready[0] if ready else None
        if objective is not None:
            self.state.set("active_objective", objective.objective_id, source="cognition-cycle")

        # The learned representation proposes an interpretation; explicit
        # structures remain authoritative state rather than being overwritten.
        interpretation = (
            self.brain.predict(observation.structure)
            if self.brain.labels
            else self.brain.representation.encode(observation.structure)
        )
        self.state.set("last_interpretation", interpretation, source="cognition-cycle")
        self.working.add(interpretation)

        action = action_selector(interpretation, objective, recent) if action_selector else None
        execution = executor(action) if action is not None and executor is not None else None
        evaluation = (
            evaluator(action, execution, observation)
            if action is not None and evaluator is not None
            else None
        )

        if world_updater is not None:
            world_updater(self.world, observation, execution, evaluation)

        learning_examples: list[StructuredExample] = [observation.structure]
        if experience_encoder is not None:
            encoded = experience_encoder(observation, action, execution, evaluation)
            if encoded is not None:
                learning_examples.append(encoded)

        learned = False
        if learning and learning_examples:
            report = self.brain.train_representation(learning_examples, epochs=1)
            learned = report.steps > 0
            self.state.set("last_learning_report", report, source="cognition-cycle")

        experience = {
            "observation": observation.value,
            "action": action,
            "execution": execution,
            "evaluation": evaluation,
            "objective_id": objective.objective_id if objective else None,
        }
        self.episodic.record(experience)
        self.semantic.set(f"cycle:{self.step_count}:experience", experience)
        self.memory.put(
            MemoryRecord(
                key=f"experience:{self.step_count}",
                value=experience,
                kind="experience",
            )
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

    def run(self, observations: Iterable[CycleObservation], **kwargs: Any) -> tuple[CycleResult, ...]:
        return tuple(self.step(item, **kwargs) for item in observations)

    def run_forever(self, observations: Iterable[CycleObservation], **kwargs: Any) -> Iterator[CycleResult]:
        for observation in observations:
            yield self.step(observation, **kwargs)
