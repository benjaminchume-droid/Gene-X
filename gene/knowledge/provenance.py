"""Provenance primitives for claims and artifacts."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

@dataclass(frozen=True, slots=True)
class Provenance:
    source: str
    method: str
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    evidence_ids: tuple[str, ...] = ()
    provenance_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)
