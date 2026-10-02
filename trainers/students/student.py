"""Generic student adapter for teacher-driven learning."""
from __future__ import annotations
from typing import Any, Protocol

class Student(Protocol):
    def attempt(self, input: Any) -> Any: ...
    def update(self, input: Any, output: Any, feedback: Any) -> None: ...

class StudentLoop:
    def __init__(self, student: Student) -> None:
        self.student = student
    def learn(self, examples, teacher):
        history = []
        for example in examples:
            output = self.student.attempt(example)
            feedback = teacher(example, output)
            self.student.update(example, output, feedback)
            history.append((example, output, feedback))
        return tuple(history)
