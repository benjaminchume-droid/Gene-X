"""Events emitted when the internal substrate changes."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

@dataclass(frozen=True)
class StateEvent:
    kind: str
    payload: dict[str, Any]
    id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
