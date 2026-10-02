"""Experience-driven training orchestration.

The trainer is deliberately domain-neutral. Teachers provide feedback, the
organism decides how its registered learning components update, and the trainer
only coordinates the transaction.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from .experience import Experience
from .organism import LearningOrganism, OrganismStep
from .signals import LearningSignal

@dataclass(frozen=True, slots=True)
class TeacherFeedback:
    signals: tuple[LearningSignal, ...]
    source: str = "teacher"

class ExperienceTrainer:
    def __init__(
        self,
        organism: LearningOrganism,
        teachers: Iterable[Callable[[Experience], Iterable[LearningSignal]]] = (),
    ) -> None:
        self.organism = organism
        self.teachers = tuple(teachers)

    def step(self, experience: Experience) -> OrganismStep:
        signals: list[LearningSignal] = []
        for teacher in self.teachers:
            signals.extend(tuple(teacher(experience)))
        return self.organism.learn(experience, signals)

    def fit(self, experiences: Iterable[Experience]) -> tuple[OrganismStep, ...]:
        return tuple(self.step(experience) for experience in experiences)
