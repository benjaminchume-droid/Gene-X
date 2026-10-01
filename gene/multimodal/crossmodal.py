"""Cross-modal correspondence primitives."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Correspondence:
    source_kind: str
    source: Any
    target_kind: str
    target: Any
    relation: str
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
