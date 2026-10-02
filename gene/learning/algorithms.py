"""Pluggable learning algorithms.

The protocol deliberately does not require gradient descent. Neural, symbolic,
reinforcement, evolutionary, or hybrid learners can implement the same contract.
"""
from __future__ import annotations

from typing import Any, Protocol


class LearningAlgorithm(Protocol):
    def update(self, state: Any, sample: Any) -> Any: ...
    def evaluate(self, state: Any, sample: Any) -> float: ...


class ExponentialMovingUpdate:
    """A tiny generic online learner useful for continuous scalar state."""

    def __init__(self, rate: float = 0.1) -> None:
        if not 0.0 < rate <= 1.0:
            raise ValueError("rate must be in (0, 1]")
        self.rate = rate

    def update(self, state: float, sample: float) -> float:
        return state + self.rate * (sample - state)

    def evaluate(self, state: float, sample: float) -> float:
        return abs(sample - state)
