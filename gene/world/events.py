"""World events as observable changes."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
@dataclass(frozen=True, slots=True)
class WorldEvent:
    event_type: str
    participants: tuple[str, ...] = ()
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: str = field(default_factory=lambda: str(uuid4()))
