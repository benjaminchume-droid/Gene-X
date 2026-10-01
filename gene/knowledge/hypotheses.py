"""Explicit hypotheses that can be tested and revised."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass
class Hypothesis:
    statement: Any
    hypothesis_id: str = field(default_factory=lambda: uuid4().hex)
    tests: list[Any] = field(default_factory=list)
    status: str = "untested"

    def add_test(self, result: Any) -> None:
        self.tests.append(result)

    def update_status(self, status: str) -> None:
        self.status = status
