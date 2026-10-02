"""Validated runtime configuration primitives."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    max_workers: int = 1
    step_timeout_seconds: float = 300.0
    checkpoint_interval: int = 100
    deterministic: bool = False
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.max_workers < 1: raise ValueError("max_workers must be positive")
        if self.step_timeout_seconds <= 0: raise ValueError("step_timeout_seconds must be positive")
        if self.checkpoint_interval < 1: raise ValueError("checkpoint_interval must be positive")
