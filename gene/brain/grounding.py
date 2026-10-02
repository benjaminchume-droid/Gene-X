"""External-experience grounding for trainable representations.

Grounding is deliberately domain-neutral: a teacher supplies target vectors
or verified pair relationships, and the representation updates toward them.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .representation import StructuredExample, TrainableRepresentation

@dataclass(frozen=True, slots=True)
class GroundedSample:
    example: StructuredExample
    target: tuple[float, ...]

@dataclass(frozen=True, slots=True)
class GroundingReport:
    steps: int
    mean_loss: float

class GroundedRepresentationTrainer:
    def __init__(self, representation: TrainableRepresentation) -> None:
        self.representation = representation

    def fit_targets(
        self,
        samples: Iterable[GroundedSample],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ) -> GroundingReport:
        batch = tuple(samples)
        if epochs < 1 or learning_rate <= 0:
            raise ValueError("invalid training configuration")
        total = 0.0
        steps = 0
        for _ in range(epochs):
            for sample in batch:
                representation = self.representation.encode(sample.example)
                target = tuple(sample.target)
                if len(target) != self.representation.representation_size:
                    raise ValueError("target dimensionality mismatch")
                error = [pred - truth for pred, truth in zip(representation.values, target)]
                loss = sum(value * value for value in error) / max(1, len(error))
                self.representation.nudge_features(
                    self.representation.feature_vector(sample.example),
                    error,
                    learning_rate,
                )
                total += loss
                steps += 1
                self.representation.training_steps += 1
        return GroundingReport(steps, total / max(1, steps))
