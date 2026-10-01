"""Event-oriented memory view."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class Episode:
    event: Any
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    context: dict[str, Any] = field(default_factory=dict)

class EpisodicMemory:
    def __init__(self) -> None:
        self._episodes: list[Episode] = []

    def record(self, event: Any, **context: Any) -> Episode:
        episode = Episode(event, context=context)
        self._episodes.append(episode)
        return episode

    def recent(self, limit: int = 10) -> tuple[Episode, ...]:
        return tuple(self._episodes[-limit:])
