"""Explicit uncertainty primitives.

Gene X must be able to represent unknown, tentative, and conflicting knowledge
instead of collapsing every proposition into true or false.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Generic, TypeVar

T = TypeVar("T")

class KnowledgeStatus(StrEnum):
    UNKNOWN = "unknown"
    HYPOTHESIS = "hypothesis"
    INFERRED = "inferred"
    SUPPORTED = "supported"
    VERIFIED = "verified"
    CONTRADICTED = "contradicted"

@dataclass(frozen=True, slots=True)
class Belief(Generic[T]):
    value: T
    status: KnowledgeStatus
    confidence: float
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
