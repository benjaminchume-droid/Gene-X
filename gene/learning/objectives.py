"""General learning signals and objectives."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class LearningSignal:
    value: float
    kind: str
    source: str | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.kind == "":
            raise ValueError("learning signal kind cannot be empty")


class LearningObjective(Protocol):
    def loss(self, prediction: Any, target: Any) -> float: ...
    def reward(self, result: Any) -> float: ...


@dataclass(frozen=True, slots=True)
class SupervisedLoss:
    """Numerically stable squared-error objective for generic scalar outputs."""

    def loss(self, prediction: float, target: float) -> float:
        error = prediction - target
        return error * error

    def reward(self, result: Any) -> float:
        return float(result)
