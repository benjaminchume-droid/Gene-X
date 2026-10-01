"""Evidence objects with explicit provenance and verification state."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from .provenance import Provenance

class EvidenceStatus(StrEnum):
    UNCHECKED = "unchecked"
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    VERIFIED = "verified"

@dataclass(slots=True)
class Evidence:
    content: Any
    provenance: Provenance
    status: EvidenceStatus = EvidenceStatus.UNCHECKED
    evidence_id: str = field(default_factory=lambda: str(uuid4()))
    notes: list[str] = field(default_factory=list)

    def mark(self, status: EvidenceStatus, note: str | None = None) -> None:
        self.status = status
        if note:
            self.notes.append(note)
