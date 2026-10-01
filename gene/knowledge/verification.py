"""Verification primitives that keep evidence separate from belief."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    evidence: Any = None
    reason: str = ""

class Verifier:
    def __init__(self, check: Callable[[Any], VerificationResult]) -> None:
        self.check = check

    def verify(self, claim: Any) -> VerificationResult:
        return self.check(claim)
