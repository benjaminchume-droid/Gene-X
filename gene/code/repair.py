"""Iterative repair state for autonomous coding work."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class RepairIteration:
    attempt: int
    failure: Any
    diagnosis: Any = None
    changes: tuple[Any, ...] = ()
    verified: bool = False

@dataclass
class RepairLoop:
    max_attempts: int = 3
    iterations: list[RepairIteration] = field(default_factory=list)

    def record(self, iteration: RepairIteration) -> None:
        if iteration.attempt < 1 or iteration.attempt != len(self.iterations) + 1:
            raise ValueError("repair attempts must be sequential and positive")
        self.iterations.append(iteration)

    @property
    def complete(self) -> bool:
        return bool(self.iterations) and self.iterations[-1].verified

    @property
    def exhausted(self) -> bool:
        return len(self.iterations) >= self.max_attempts and not self.complete

    def next_attempt(self) -> int | None:
        if self.complete or self.exhausted:
            return None
        return len(self.iterations) + 1
