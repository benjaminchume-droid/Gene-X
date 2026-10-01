"""Curriculum ordering based on explicit task metadata."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Lesson:
    task: Any
    difficulty: float = 0.0

class Curriculum:
    def __init__(self) -> None:
        self._lessons: list[Lesson] = []

    def add(self, task: Any, difficulty: float = 0.0) -> None:
        self._lessons.append(Lesson(task, difficulty))

    def ordered(self) -> tuple[Lesson, ...]:
        return tuple(sorted(self._lessons, key=lambda lesson: lesson.difficulty))
