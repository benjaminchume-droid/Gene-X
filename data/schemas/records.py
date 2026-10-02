"""Serializable neutral dataset records."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class Record:
    record_id: str
    input: Any
    target: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"record_id": self.record_id, "input": self.input, "target": self.target, "metadata": self.metadata}
