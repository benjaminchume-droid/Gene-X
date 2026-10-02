"""Shared training runtime primitives.

The runtime is substrate-agnostic: datasets, learners, evaluators, and
checkpoint stores are injected. It contains no domain-specific curriculum.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Protocol

@dataclass(frozen=True, slots=True)
class TrainingExample:
    input: Any
    target: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class TrainingStep:
    epoch: int
    index: int
    loss: float | None
    metrics: dict[str, float] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class TrainingReport:
    steps: tuple[TrainingStep, ...]
    stopped_early: bool = False
    reason: str | None = None

class Trainable(Protocol):
    def learn(self, example: TrainingExample) -> float | None: ...

class StepObserver(Protocol):
    def __call__(self, step: TrainingStep) -> None: ...

class TrainingRuntime:
    def __init__(self, learner: Trainable, *, observer: StepObserver | None = None) -> None:
        self.learner = learner
        self.observer = observer

    def run(
        self,
        dataset: Iterable[TrainingExample],
        *,
        epochs: int = 1,
        stop: Callable[[TrainingStep], bool] | None = None,
    ) -> TrainingReport:
        if epochs < 1:
            raise ValueError("epochs must be positive")
        examples = tuple(dataset)
        history: list[TrainingStep] = []
        for epoch in range(epochs):
            for index, example in enumerate(examples):
                loss = self.learner.learn(example)
                step = TrainingStep(epoch, index, loss)
                history.append(step)
                if self.observer:
                    self.observer(step)
                if stop and stop(step):
                    return TrainingReport(tuple(history), True, "stop predicate")
        return TrainingReport(tuple(history))
