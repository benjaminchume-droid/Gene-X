"""Convert raw inputs into explicit observations without pretending certainty."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class Observation:
    value: Any
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)

def understand(value: Any, *, source: str = "input", metadata: dict[str, Any] | None = None) -> Observation:
    return Observation(value=value, source=source, metadata=dict(metadata or {}))
