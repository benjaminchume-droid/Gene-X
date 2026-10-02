"""Training orchestration for representation and task learning."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .model import GeneBrain
from .representation import StructuredExample


@dataclass(frozen=True)
class TrainingSample:
    input: StructuredExample
    target: str


@dataclass(frozen=True)
class RepresentationSample:
    input: StructuredExample


@dataclass(frozen=True)
class SimilaritySample:
    left: StructuredExample
    right: StructuredExample
    similarity: float


@dataclass(frozen=True)
class TrainingReport:
    epochs: int
    losses: tuple[float, ...]
    samples: int


class BrainTrainer:
    """Single entry point for trainable Gene learning."""

    def __init__(self, brain: GeneBrain) -> None:
        self.brain = brain

    def fit(
        self,
        samples: Iterable[TrainingSample],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ) -> TrainingReport:
        items = [(s.input, s.target) for s in samples]
        losses = self.brain.train(items, epochs=epochs, learning_rate=learning_rate)
        return TrainingReport(epochs, tuple(losses), len(items))

    def fit_representation(
        self,
        samples: Iterable[RepresentationSample | StructuredExample],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ):
        examples = [
            sample.input if isinstance(sample, RepresentationSample) else sample
            for sample in samples
        ]
        return self.brain.train_representation(
            examples, epochs=epochs, learning_rate=learning_rate
        )

    def fit_pairs(
        self,
        samples: Iterable[SimilaritySample],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ):
        pairs = [(sample.left, sample.right, sample.similarity) for sample in samples]
        return self.brain.train_pairs(pairs, epochs=epochs, learning_rate=learning_rate)
