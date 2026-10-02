"""Learning signals and provenance for non-token-centric training.

A signal is an observation about an attempted transition. It can come from a
human, another model, a compiler, a test, a tool, an environment, or a formal
checker. No domain knowledge is embedded here.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4

class SignalKind(str, Enum):
    REWARD = "reward"
    CORRECTION = "correction"
    DEMONSTRATION = "demonstration"
    VERIFICATION = "verification"
    OBSERVATION = "observation"
    PREFERENCE = "preference"
    ERROR = "error"

@dataclass(frozen=True)
class LearningSignal:
    kind: SignalKind
    value: float | None = None
    target: Any = None
    source: str = "environment"
    confidence: float = 1.0
    provenance: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
    signal_id: str = field(default_factory=lambda: uuid4().hex)

    def normalized_confidence(self) -> float:
        return max(0.0, min(1.0, self.confidence))

@dataclass(frozen=True)
class LearningOutcome:
    improved: bool
    delta: float
    learned: tuple[str, ...] = ()
    retained: tuple[str, ...] = ()
    discarded: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
