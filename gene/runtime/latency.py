"""Latency-aware cognitive scheduling primitives."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from time import perf_counter
from typing import Any, Callable

class CognitiveMode(str, Enum):
    REFLEX="reflex"
    CONVERSATIONAL="conversational"
    DEEP="deep"

@dataclass(frozen=True, slots=True)
class LatencyBudget:
    first_response_seconds: float
    internal_budget_seconds: float
    mode: CognitiveMode

@dataclass(frozen=True, slots=True)
class TimedResult:
    value: Any
    elapsed_seconds: float
    mode: CognitiveMode

class LatencyController:
    def __init__(self, *, reflex_limit: float=.12, conversational_limit: float=2.0) -> None:
        if reflex_limit<=0 or conversational_limit<=reflex_limit: raise ValueError("latency limits must be positive and ordered")
        self.reflex_limit=reflex_limit; self.conversational_limit=conversational_limit
    def classify(self, *, complexity: float, requires_action: bool=False, requires_external_io: bool=False) -> LatencyBudget:
        score=max(0.0,float(complexity))
        if not requires_action and not requires_external_io and score<=1.0:
            return LatencyBudget(self.reflex_limit,self.reflex_limit,CognitiveMode.REFLEX)
        if not requires_action and score<=4.0:
            return LatencyBudget(self.conversational_limit,self.conversational_limit,CognitiveMode.CONVERSATIONAL)
        return LatencyBudget(float("inf"),float("inf"),CognitiveMode.DEEP)
    def time(self, fn: Callable[[],Any], mode: CognitiveMode) -> TimedResult:
        started=perf_counter(); value=fn()
        return TimedResult(value,perf_counter()-started,mode)
