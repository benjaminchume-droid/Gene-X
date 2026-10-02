"""Unified experience-driven learning organism.

Gene does not require a single neural parameter tensor to constitute learning.
This engine coordinates representation updates, skill/procedure acquisition,
memory consolidation, routing adaptation, and replay. Neural optimizers can be
attached as one learner among many.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Protocol
from .experience import Experience
from .signals import LearningSignal, LearningOutcome

class LearnerComponent(Protocol):
    def learn(self, experience: Experience, signals: tuple[LearningSignal, ...]) -> LearningOutcome: ...

@dataclass
class OrganismStep:
    experience: Experience
    signals: tuple[LearningSignal, ...]
    outcomes: tuple[LearningOutcome, ...]
    score: float

@dataclass
class LearningOrganism:
    components: list[LearnerComponent] = field(default_factory=list)
    history: list[OrganismStep] = field(default_factory=list)
    step_count: int = 0

    def add(self, component: LearnerComponent) -> None:
        self.components.append(component)

    def learn(self, experience: Experience, signals: Iterable[LearningSignal]) -> OrganismStep:
        batch = tuple(signals)
        outcomes = tuple(c.learn(experience, batch) for c in self.components)
        values = [o.delta for o in outcomes]
        score = sum(values) / len(values) if values else 0.0
        step = OrganismStep(experience, batch, outcomes, score)
        self.history.append(step)
        self.step_count += 1
        return step

    def replay(self, experiences: Iterable[tuple[Experience, Iterable[LearningSignal]]]) -> tuple[OrganismStep, ...]:
        return tuple(self.learn(e, s) for e, s in experiences)

class SignalFromEvaluator:
    """Adapter turning an arbitrary evaluator into a learning signal source."""

    def __init__(self, evaluator: Callable[[Experience], Any]):
        self.evaluator = evaluator

    def __call__(self, experience: Experience) -> tuple[LearningSignal, ...]:
        result = self.evaluator(experience)
        if isinstance(result, LearningSignal):
            return (result,)
        if isinstance(result, (tuple, list)):
            return tuple(result)
        return (LearningSignal(kind="observation", value=float(result), source="evaluator"),)
