"""Runtime bridge from action/evaluation to continual learning."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from gene.learning.organism import LearningOrganism
from gene.learning.signals import LearningSignal
from gene.learning.experience import Experience

@dataclass
class LearningLoop:
    organism: LearningOrganism
    evaluator: Callable[[Any, Any], tuple[LearningSignal, ...]]

    def observe(self, experience: Experience) -> Any:
        signals = self.evaluator(experience.input, experience.outcome)
        return self.organism.learn(experience, signals)

    def run(self, experiences: list[Experience]) -> tuple[Any, ...]:
        return tuple(self.observe(e) for e in experiences)
