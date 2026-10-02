"""Teacher-to-student transfer without assuming either is a neural model."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True, slots=True)
class DistillationStep:
    input: Any
    teacher_output: Any
    student_output: Any
    feedback: Any

class DistillationLoop:
    def __init__(self, teacher: Callable[[Any], Any], student: Any, compare: Callable[[Any, Any], Any]) -> None:
        self.teacher, self.student, self.compare = teacher, student, compare

    def run(self, inputs: Iterable[Any]) -> tuple[DistillationStep, ...]:
        history = []
        for value in inputs:
            teacher_output = self.teacher(value)
            student_output = self.student.attempt(value)
            feedback = self.compare(teacher_output, student_output)
            self.student.update(value, student_output, feedback)
            history.append(DistillationStep(value, teacher_output, student_output, feedback))
        return tuple(history)
