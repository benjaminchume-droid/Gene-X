"""Resource-aware provider loading with idempotent reservations."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol

class Loadable(Protocol):
    name: str
    def load(self, **kwargs: Any) -> None: ...
    def unload(self) -> None: ...

@dataclass
class ResourceLedger:
    memory_limit_mb: int | None = None
    memory_used_mb: int = 0
    loaded: set[str] = field(default_factory=set)

    def can_reserve(self, memory_mb: int) -> bool:
        if memory_mb < 0:
            raise ValueError("memory_mb cannot be negative")
        return self.memory_limit_mb is None or self.memory_used_mb + memory_mb <= self.memory_limit_mb

    def reserve(self, name: str, memory_mb: int) -> None:
        if name in self.loaded:
            return
        if not self.can_reserve(memory_mb):
            raise MemoryError(f"memory budget exceeded while loading {name}")
        self.memory_used_mb += memory_mb
        self.loaded.add(name)

    def release(self, name: str, memory_mb: int) -> None:
        if name in self.loaded:
            self.loaded.remove(name)
            self.memory_used_mb = max(0, self.memory_used_mb - max(0, memory_mb))

@dataclass
class ProviderLoader:
    ledger: ResourceLedger
    sizes_mb: dict[str, int] = field(default_factory=dict)

    def load(self, provider: Loadable, **kwargs: Any) -> None:
        size = self.sizes_mb.get(provider.name, 0)
        if provider.name in self.ledger.loaded:
            return
        self.ledger.reserve(provider.name, size)
        try:
            provider.load(**kwargs)
        except Exception:
            self.ledger.release(provider.name, size)
            raise

    def unload(self, provider: Loadable) -> None:
        if provider.name not in self.ledger.loaded:
            return
        provider.unload()
        self.ledger.release(provider.name, self.sizes_mb.get(provider.name, 0))
