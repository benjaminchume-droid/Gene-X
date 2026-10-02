"""Capability and execution policy primitives."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable

@dataclass(frozen=True)
class CapabilityGrant:
    capability: str
    scope: str
    expires_at: float | None = None

@dataclass
class Policy:
    allowed: set[str] = field(default_factory=set)
    denied: set[str] = field(default_factory=set)
    grants: list[CapabilityGrant] = field(default_factory=list)

    def check(self, capability: str) -> bool:
        if capability in self.denied:
            return False
        return capability in self.allowed or any(g.capability == capability for g in self.grants)

    def require(self, capability: str) -> None:
        if not self.check(capability):
            raise PermissionError(f"capability denied: {capability}")
