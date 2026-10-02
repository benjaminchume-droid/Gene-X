"""Adapters that let existing Gene primitives participate in organism learning."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from .experience import Experience
from .signals import LearningSignal, LearningOutcome

@dataclass
class RepresentationAdapter:
    update: Callable[[Any, Any, float], Any]
    state: Any
    def learn(self, experience: Experience, signals: tuple[LearningSignal, ...]) -> LearningOutcome:
        reward = _signal_value(signals)
        before = self.state
        self.state = self.update(self.state, experience, reward)
        return LearningOutcome(self.state != before, reward, ("representation",))

@dataclass
class ProcedureAdapter:
    procedures: dict[str, Any] = field(default_factory=dict)
    def learn(self, experience: Experience, signals: tuple[LearningSignal, ...]) -> LearningOutcome:
        reward = _signal_value(signals)
        key = str(experience.input)
        if reward > 0 and experience.outcome is not None:
            self.procedures[key] = experience.outcome
            return LearningOutcome(True, reward, (key,))
        return LearningOutcome(False, reward)

@dataclass
class RoutingAdapter:
    scores: dict[str, float] = field(default_factory=dict)
    rate: float = 0.05
    def learn(self, experience: Experience, signals: tuple[LearningSignal, ...]) -> LearningOutcome:
        component = str(experience.source)
        reward = _signal_value(signals)
        old = self.scores.get(component, 0.0)
        self.scores[component] = old + self.rate * (reward - old)
        return LearningOutcome(True, self.scores[component] - old, (component,))

def _signal_value(signals: tuple[LearningSignal, ...]) -> float:
    vals = [s.value for s in signals if s.value is not None]
    return sum(vals) / len(vals) if vals else 0.0
