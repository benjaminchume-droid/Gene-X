"""Memory importance and retention scoring."""
from __future__ import annotations
from dataclasses import dataclass
from math import exp
from typing import Any

@dataclass(frozen=True)
class MemoryScore:
    salience: float
    novelty: float
    utility: float
    confidence: float

    @property
    def total(self) -> float:
        return max(0.0, min(1.0, 0.3*self.salience + 0.25*self.novelty + 0.3*self.utility + 0.15*self.confidence))

class ImportanceModel:
    def score(self, item: Any, *, salience: float=0.0, novelty: float=0.0, utility: float=0.0, confidence: float=1.0) -> MemoryScore:
        return MemoryScore(*[max(0.0, min(1.0, x)) for x in (salience, novelty, utility, confidence)])

    def retention(self, score: MemoryScore, age: float, decay: float = 0.001) -> float:
        return score.total * exp(-max(0.0, age) * max(0.0, decay))
