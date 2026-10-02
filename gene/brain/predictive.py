"""Small trainable predictive substrate for structured cognition.

The predictor learns a continuous transition from an input representation and
an action representation to a resulting representation. It does not contain
domain labels or fixed semantic rules.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import tanh
from random import Random
from typing import Iterable

@dataclass(frozen=True, slots=True)
class PredictionReport:
    steps: int
    mean_loss: float

class PredictiveCore:
    def __init__(self, input_size: int, action_size: int, output_size: int, seed: int = 7) -> None:
        if min(input_size, action_size, output_size) < 1:
            raise ValueError("dimensions must be positive")
        self.input_size, self.action_size, self.output_size = input_size, action_size, output_size
        rng = Random(seed)
        width = input_size + action_size
        scale = 1.0 / max(1, width) ** 0.5
        self.weights = [[rng.uniform(-scale, scale) for _ in range(width)] for _ in range(output_size)]
        self.bias = [0.0] * output_size

    def predict(self, state: Iterable[float], action: Iterable[float]) -> tuple[float, ...]:
        state, action = tuple(state), tuple(action)
        if len(state) != self.input_size or len(action) != self.action_size:
            raise ValueError("input dimensionality mismatch")
        values = state + action
        return tuple(tanh(sum(w*x for w,x in zip(row, values)) + b) for row,b in zip(self.weights, self.bias))

    def fit(self, samples: Iterable[tuple[Iterable[float], Iterable[float], Iterable[float]]], *, epochs: int = 1, learning_rate: float = 0.01) -> PredictionReport:
        batch = [(tuple(s), tuple(a), tuple(t)) for s,a,t in samples]
        if epochs < 1 or learning_rate <= 0:
            raise ValueError("epochs must be positive and learning_rate must be positive")
        total = 0.0
        steps = 0
        for _ in range(epochs):
            for state, action, target in batch:
                if len(target) != self.output_size:
                    raise ValueError("target dimensionality mismatch")
                values = state + action
                prediction = self.predict(state, action)
                for k,(pred,truth) in enumerate(zip(prediction,target)):
                    error = pred-truth
                    total += error*error
                    gradient = 2.0*error*(1.0-pred*pred)
                    for j,value in enumerate(values):
                        self.weights[k][j] -= learning_rate*gradient*value
                    self.bias[k] -= learning_rate*gradient
                steps += 1
        return PredictionReport(steps, total / max(1, steps*self.output_size))
