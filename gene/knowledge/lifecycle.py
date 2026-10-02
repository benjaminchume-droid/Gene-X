"""Evidence-aware knowledge lifecycle."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable
from .facts import Fact, FactStore
from .verification import VerificationResult

@dataclass
class KnowledgeCandidate:
    fact: Fact
    evidence: tuple[Any, ...] = ()
    verified: bool = False
    rejected: bool = False

@dataclass
class KnowledgeLifecycle:
    store: FactStore
    candidates: dict[str, KnowledgeCandidate] = field(default_factory=dict)
    def propose(self, fact: Fact, evidence: Iterable[Any] = ()) -> KnowledgeCandidate:
        candidate = KnowledgeCandidate(fact, tuple(evidence))
        self.candidates[fact.fact_id] = candidate
        return candidate
    def resolve(self, fact_id: str, verification: VerificationResult) -> KnowledgeCandidate:
        candidate = self.candidates[fact_id]
        candidate.verified = verification.verified
        candidate.rejected = not candidate.verified
        if candidate.verified:
            self.store.add(candidate.fact)
        return candidate
