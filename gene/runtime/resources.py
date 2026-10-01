"""Runtime resource accounting independent of any specific hardware."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ResourceUsage:
    cpu_seconds: float = 0.0
    memory_mb: float = 0.0
    storage_mb: float = 0.0
    gpu_seconds: float = 0.0

    def add(self, other: "ResourceUsage") -> None:
        self.cpu_seconds += other.cpu_seconds
        self.memory_mb += other.memory_mb
        self.storage_mb += other.storage_mb
        self.gpu_seconds += other.gpu_seconds

@dataclass(frozen=True)
class ResourceLimits:
    cpu_seconds: float | None = None
    memory_mb: float | None = None
    storage_mb: float | None = None
    gpu_seconds: float | None = None

    def allows(self, usage: ResourceUsage) -> bool:
        checks = (
            (self.cpu_seconds, usage.cpu_seconds),
            (self.memory_mb, usage.memory_mb),
            (self.storage_mb, usage.storage_mb),
            (self.gpu_seconds, usage.gpu_seconds),
        )
        return all(limit is None or value <= limit for limit, value in checks)
