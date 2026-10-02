"""Adaptive curriculum execution without embedded subject matter."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable

@dataclass(frozen=True, slots=True)
class Lesson:
    lesson_id: str
    payload: object
    prerequisites: tuple[str, ...] = ()

@dataclass(frozen=True, slots=True)
class LessonOutcome:
    lesson_id: str
    score: float
    completed: bool

class CurriculumEngine:
    def __init__(self, lessons: Iterable[Lesson]) -> None:
        self.lessons = {x.lesson_id: x for x in lessons}
        self.outcomes: dict[str, LessonOutcome] = {}

    def ready(self) -> tuple[Lesson, ...]:
        completed = {k for k, v in self.outcomes.items() if v.completed}
        return tuple(x for x in self.lessons.values() if x.lesson_id not in self.outcomes and set(x.prerequisites) <= completed)

    def teach(self, lesson_id: str, learner: Callable[[object], float]) -> LessonOutcome:
        lesson = self.lessons[lesson_id]
        if lesson not in self.ready():
            raise ValueError("lesson prerequisites are not satisfied")
        score = float(learner(lesson.payload))
        outcome = LessonOutcome(lesson_id, score, score >= 0.0)
        self.outcomes[lesson_id] = outcome
        return outcome
