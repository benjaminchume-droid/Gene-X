"""Event primitives used to observe and coordinate Gene X."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
from uuid import uuid4

@dataclass(frozen=True, slots=True)
class Event:
    kind: str
    payload: Mapping[str, Any] = field(default_factory=dict)
    source: str = "runtime"
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class EventBus:
    """In-process event bus. Delivery is synchronous and deterministic."""

    def __init__(self) -> None:
        self._handlers: dict[str, list] = {}

    def subscribe(self, kind: str, handler) -> None:
        self._handlers.setdefault(kind, []).append(handler)

    def publish(self, event: Event) -> None:
        for handler in tuple(self._handlers.get(event.kind, ())):
            handler(event)

    def clear(self, kind: str | None = None) -> None:
        if kind is None:
            self._handlers.clear()
        else:
            self._handlers.pop(kind, None)
