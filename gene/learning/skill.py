"""Skills as reusable capability records with evidence."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Skill:
    name: str
    capability: str
    proficiency: float = 0.0
    evidence: list[Any] = field(default_factory=list)

    def update(self, score: float, evidence: Any = None) -> None:
        if not 0.0 <= score <= 1.0:
            raise ValueError("score must be between 0 and 1")
        self.proficiency = score if not self.evidence else (self.proficiency + score) / 2
        if evidence is not None:
            self.evidence.append(evidence)
