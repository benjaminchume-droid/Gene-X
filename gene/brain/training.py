"""Training orchestration for the hybrid brain."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .model import GeneBrain
from .representation import StructuredExample


@dataclass(frozen=True)
class TrainingSample:
    input: StructuredExample
    target: str


@dataclass(frozen=True)
class TrainingReport:
    epochs: int
    losses: tuple[float, ...]
    samples: int


class BrainTrainer:
    def __init__(self, brain: GeneBrain) -> None:
        self.brain = brain

    def fit(self, samples: Iterable[TrainingSample], *, epochs: int = 1, learning_rate: float = 0.03) -> TrainingReport:
        items = [(s.input, s.target) for s in samples]
        losses = self.brain.train(items, epochs=epochs, learning_rate=learning_rate)
        return TrainingReport(epochs=epochs, losses=tuple(losses), samples=len(items))
