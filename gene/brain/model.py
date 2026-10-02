"""Learned cognitive substrate built on the adaptive representation system."""
from __future__ import annotations

from dataclasses import dataclass
from math import exp
from random import Random
from typing import Iterable

from .representation import (
    FeatureVector,
    Representation,
    StructuredExample,
    TrainableRepresentation,
    encode_structure,
)


@dataclass(frozen=True)
class BrainOutput:
    label: str
    probabilities: dict[str, float]
    confidence: float
    representation: Representation


class GeneBrain:
    """Trainable hybrid brain.

    The representation is independently trainable and reusable. The optional
    supervised head learns a task over that representation; it is not the
    representation itself and does not define Gene's knowledge.
    """

    def __init__(
        self,
        *,
        input_size: int = 8192,
        embedding_size: int = 48,
        representation_size: int = 128,
        seed: int = 7,
    ) -> None:
        self.representation = TrainableRepresentation(
            input_size=input_size,
            embedding_size=embedding_size,
            representation_size=representation_size,
            seed=seed,
        )
        self.labels: list[str] = []
        self._rng = Random(seed + 1)
        self.head: list[list[float]] = []
        self.head_bias: list[float] = []

    def _ensure_labels(self, labels: Iterable[str]) -> None:
        for label in labels:
            if label in self.labels:
                continue
            self.labels.append(label)
            scale = 1.0 / max(1, self.representation.representation_size) ** 0.5
            self.head.append([
                self._rng.uniform(-scale, scale)
                for _ in range(self.representation.representation_size)
            ])
            self.head_bias.append(0.0)

    def _softmax(self, logits: list[float]) -> list[float]:
        if not logits:
            return []
        maximum = max(logits)
        values = [exp(min(40.0, value - maximum)) for value in logits]
        total = sum(values)
        return [value / total for value in values]

    def predict(self, example: StructuredExample | FeatureVector) -> BrainOutput:
        if not self.labels:
            raise RuntimeError("brain has no supervised labels; train a head first")
        representation = self.representation.encode(example)
        logits = [
            sum(w * x for w, x in zip(row, representation.values)) + bias
            for row, bias in zip(self.head, self.head_bias)
        ]
        probabilities = self._softmax(logits)
        index = max(range(len(probabilities)), key=probabilities.__getitem__)
        return BrainOutput(
            self.labels[index],
            dict(zip(self.labels, probabilities)),
            probabilities[index],
            representation,
        )

    def train_representation(
        self,
        examples: Iterable[StructuredExample],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ):
        return self.representation.train_autoencoding(
            examples, epochs=epochs, learning_rate=learning_rate
        )

    def train_pairs(
        self,
        pairs: Iterable[tuple[StructuredExample, StructuredExample, float]],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ):
        return self.representation.train_pairs(
            pairs, epochs=epochs, learning_rate=learning_rate
        )

    def train(
        self,
        examples: Iterable[tuple[StructuredExample, str]],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ) -> list[float]:
        batch = list(examples)
        if not batch:
            return []
        self._ensure_labels(label for _, label in batch)
        losses: list[float] = []
        for _ in range(epochs):
            total = 0.0
            for example, target in batch:
                representation = self.representation.encode(example)
                logits = [
                    sum(w * x for w, x in zip(row, representation.values)) + bias
                    for row, bias in zip(self.head, self.head_bias)
                ]
                probabilities = self._softmax(logits)
                target_i = self.labels.index(target)
                loss = -__import__("math").log(max(probabilities[target_i], 1e-12))
                grad = probabilities[:]
                grad[target_i] -= 1.0
                for i, g in enumerate(grad):
                    self.head_bias[i] -= learning_rate * g
                    for j in range(len(self.head[i])):
                        self.head[i][j] -= learning_rate * g * representation.values[j]
                total += loss
            losses.append(total / len(batch))
        return losses

    def state_dict(self) -> dict:
        return {
            "representation": self.representation.state_dict(),
            "labels": self.labels[:],
            "head": [row[:] for row in self.head],
            "head_bias": self.head_bias[:],
        }

    @classmethod
    def from_state_dict(cls, state: dict) -> "GeneBrain":
        representation = TrainableRepresentation.from_state_dict(state["representation"])
        obj = cls(
            input_size=representation.input_size,
            embedding_size=representation.embedding_size,
            representation_size=representation.representation_size,
        )
        obj.representation = representation
        obj.labels = list(state.get("labels", []))
        obj.head = [list(row) for row in state.get("head", [])]
        obj.head_bias = list(state.get("head_bias", []))
        return obj


__all__ = ["BrainOutput", "FeatureVector", "StructuredExample", "GeneBrain", "TrainableRepresentation", "encode_structure"]
