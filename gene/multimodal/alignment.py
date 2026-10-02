"""Learned cross-modal alignment without modality-specific vocabulary.

Each modality supplies numeric representations through its own encoder. The
aligner learns projection matrices from paired observations and exposes a
shared space for downstream cognition.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from random import Random
from typing import Iterable, Sequence

@dataclass(frozen=True, slots=True)
class AlignmentSample:
    source: tuple[float, ...]
    target: tuple[float, ...]

@dataclass(frozen=True, slots=True)
class AlignmentReport:
    steps: int
    mean_loss: float

class CrossModalAligner:
    def __init__(self, source_size: int, target_size: int, shared_size: int = 32, seed: int = 7) -> None:
        if min(source_size, target_size, shared_size) < 1:
            raise ValueError("dimensions must be positive")
        self.source_size, self.target_size, self.shared_size = source_size, target_size, shared_size
        rng = Random(seed)
        scale = 1.0 / sqrt(max(source_size, target_size))
        self.source_projection = [[rng.uniform(-scale, scale) for _ in range(source_size)] for _ in range(shared_size)]
        self.target_projection = [[rng.uniform(-scale, scale) for _ in range(target_size)] for _ in range(shared_size)]

    @staticmethod
    def _project(matrix: Sequence[Sequence[float]], vector: Sequence[float]) -> list[float]:
        if not vector:
            return [0.0] * len(matrix)
        return [sum(w * x for w, x in zip(row, vector)) for row in matrix]

    def encode_source(self, vector: Iterable[float]) -> tuple[float, ...]:
        values = tuple(vector)
        if len(values) != self.source_size:
            raise ValueError("source dimensionality mismatch")
        return tuple(self._project(self.source_projection, values))

    def encode_target(self, vector: Iterable[float]) -> tuple[float, ...]:
        values = tuple(vector)
        if len(values) != self.target_size:
            raise ValueError("target dimensionality mismatch")
        return tuple(self._project(self.target_projection, values))

    def similarity(self, source: Iterable[float], target: Iterable[float]) -> float:
        left, right = self.encode_source(source), self.encode_target(target)
        denom = sqrt(sum(x*x for x in left) * sum(x*x for x in right))
        return sum(x*y for x,y in zip(left,right)) / denom if denom else 0.0

    def fit(self, samples: Iterable[AlignmentSample], *, epochs: int = 1, learning_rate: float = 0.01) -> AlignmentReport:
        batch = tuple(samples)
        if epochs < 1 or learning_rate <= 0:
            raise ValueError("epochs must be positive and learning_rate must be positive")
        total = 0.0
        steps = 0
        for _ in range(epochs):
            for sample in batch:
                source, target = tuple(sample.source), tuple(sample.target)
                if len(source) != self.source_size or len(target) != self.target_size:
                    raise ValueError("sample dimensionality mismatch")
                left, right = self.encode_source(source), self.encode_target(target)
                delta = [a-b for a,b in zip(left,right)]
                loss = sum(x*x for x in delta) / max(1, self.shared_size)
                for k, error in enumerate(delta):
                    for j, value in enumerate(source):
                        self.source_projection[k][j] -= learning_rate * 2.0 * error * value / max(1, self.shared_size)
                    for j, value in enumerate(target):
                        self.target_projection[k][j] += learning_rate * 2.0 * error * value / max(1, self.shared_size)
                total += loss
                steps += 1
        return AlignmentReport(steps, total / max(1, steps))
