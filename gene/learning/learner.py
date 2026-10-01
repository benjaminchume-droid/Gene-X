"""Closed-loop learning orchestration."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .student import Student
from .teacher import Teacher
from .evaluator import Evaluator, Evaluation
from .experience import Experience

@dataclass(frozen=True)
class LearningResult:
    attempt: Any
    evaluation: Evaluation

class Learner:
    def __init__(self, student: Student, teacher: Teacher, evaluator: Evaluator) -> None:
        self.student = student
        self.teacher = teacher
        self.evaluator = evaluator

    def learn_from(self, task: Any, expected: Any, context: Any = None) -> LearningResult:
        attempt = self.student.attempt(task, context)
        teacher_feedback = self.teacher.teach(attempt, context)
        evaluation = self.evaluator.evaluate(expected, attempt)
        feedback = evaluation.feedback if evaluation.feedback is not None else teacher_feedback
        self.student.learn(Experience(task, attempt, evaluation.passed, "learning-loop"), feedback)
        return LearningResult(attempt, evaluation)
