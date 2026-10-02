"""A small, real trainable hybrid model.

The learned component is a neural function over structured features. It is
surrounded by explicit state and context so the whole system does not reduce
to next-token prediction.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, tanh
from random import Random
from typing import Iterable

from .representation import FeatureVector, StructuredExample, encode_structure


@dataclass(frozen=True)
class BrainOutput:
    label: str
    probabilities: dict[str, float]
    confidence: float


class GeneBrain:
    """One-hidden-layer classifier used as the first trainable neural substrate.

    It intentionally has no tokenizer dependency. A richer specialist can later
    replace this component behind the same interface.
    """

    def __init__(self, *, input_size: int = 4096, hidden_size: int = 96, seed: int = 7) -> None:
        if input_size < 64 or hidden_size < 4:
            raise ValueError("invalid model dimensions")
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.labels: list[str] = []
        self._rng = Random(seed)
        scale = (2.0 / input_size) ** 0.5
        self.w1 = [[self._rng.uniform(-scale, scale) for _ in range(input_size)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size
        self.w2: list[list[float]] = []
        self.b2: list[float] = []

    def _ensure_labels(self, labels: Iterable[str]) -> None:
        for label in labels:
            if label in self.labels:
                continue
            old = len(self.labels)
            self.labels.append(label)
            self.w2.append([self._rng.uniform(-0.05, 0.05) for _ in range(self.hidden_size)])
            self.b2.append(0.0)
            if old == 0:
                continue

    def _hidden(self, x: FeatureVector) -> list[float]:
        hidden = []
        for row, bias in zip(self.w1, self.b1):
            value = bias
            for i, v in x.items():
                value += row[i] * v
            hidden.append(tanh(value))
        return hidden

    def _softmax(self, logits: list[float]) -> list[float]:
        if not logits:
            return []
        m = max(logits)
        exps = [exp(min(40.0, z - m)) for z in logits]
        total = sum(exps)
        return [v / total for v in exps]

    def predict(self, example: StructuredExample | FeatureVector) -> BrainOutput:
        if not self.labels:
            raise RuntimeError("brain has no learned labels")
        x = example if isinstance(example, FeatureVector) else encode_structure(example, self.input_size)
        h = self._hidden(x)
        probs = self._softmax([sum(w * a for w, a in zip(row, h)) + b for row, b in zip(self.w2, self.b2)])
        idx = max(range(len(probs)), key=probs.__getitem__)
        return BrainOutput(self.labels[idx], dict(zip(self.labels, probs)), probs[idx])

    def train_step(self, x: FeatureVector, target: str, learning_rate: float = 0.03) -> float:
        """Perform one real gradient update and return cross-entropy loss."""
        if target not in self.labels:
            self._ensure_labels([target])
        h = self._hidden(x)
        logits = [sum(w * a for w, a in zip(row, h)) + b for row, b in zip(self.w2, self.b2)]
        probs = self._softmax(logits)
        target_i = self.labels.index(target)
        loss = -__import__("math").log(max(probs[target_i], 1e-12))

        grad_logits = probs[:]
        grad_logits[target_i] -= 1.0
        grad_h = [0.0] * self.hidden_size
        old_w2 = [row[:] for row in self.w2]
        for j, g in enumerate(grad_logits):
            self.b2[j] -= learning_rate * g
            for k in range(self.hidden_size):
                grad_h[k] += g * old_w2[j][k]
                self.w2[j][k] -= learning_rate * g * h[k]

        for k, gh in enumerate(grad_h):
            dz = gh * (1.0 - h[k] * h[k])
            self.b1[k] -= learning_rate * dz
            for i, v in x.items():
                self.w1[k][i] -= learning_rate * dz * v
        return loss

    def train(self, examples: Iterable[tuple[StructuredExample, str]], *, epochs: int = 1, learning_rate: float = 0.03) -> list[float]:
        examples = list(examples)
        if not examples:
            return []
        self._ensure_labels(label for _, label in examples)
        losses: list[float] = []
        for _ in range(epochs):
            total = 0.0
            for example, target in examples:
                total += self.train_step(encode_structure(example, self.input_size), target, learning_rate)
            losses.append(total / len(examples))
        return losses
