"""Persistent state store used by cognition and perception systems."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime, timezone

@dataclass(frozen=True)
class StateValue:
    key: str
    value: Any
    source: str | None = None
    confidence: float = 1.0
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class StateStore:
    values: dict[str, StateValue] = field(default_factory=dict)

    def set(self, key: str, value: Any, *, source: str | None = None, confidence: float = 1.0) -> StateValue:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        item = StateValue(key, value, source, confidence)
        self.values[key] = item
        return item

    def get(self, key: str) -> StateValue | None:
        return self.values.get(key)

    def snapshot(self) -> dict[str, Any]:
        return {k: v.value for k, v in self.values.items()}
