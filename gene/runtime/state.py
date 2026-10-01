"""Runtime state primitives for Gene X.

State is explicit, typed, serializable, and independent of any model.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(slots=True)
class RuntimeState:
    """Mutable runtime state with explicit versioning."""

    values: dict[str, Any] = field(default_factory=dict)
    version: int = 0
    state_id: str = field(default_factory=lambda: str(uuid4()))
    updated_at: datetime = field(default_factory=utc_now)

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.values[key] = value
        self.version += 1
        self.updated_at = utc_now()

    def update(self, values: Mapping[str, Any]) -> None:
        if not values:
            return
        self.values.update(values)
        self.version += 1
        self.updated_at = utc_now()

    def snapshot(self) -> dict[str, Any]:
        return {"state_id": self.state_id, "version": self.version,
                "updated_at": self.updated_at.isoformat(),
                "values": dict(self.values)}
