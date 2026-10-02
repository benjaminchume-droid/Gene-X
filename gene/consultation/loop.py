"""Consult -> attempt -> verify -> learn procedure loop."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from .manager import ConsultationManager, ConsultationRequest, ConsultationResult

@dataclass(frozen=True, slots=True)
class ConsultationAttempt:
    consultation: tuple[ConsultationResult,...]
    candidate: Any
    execution: Any
    verified: bool
    evidence: Any=None

class ConsultativeLoop:
    def __init__(self,manager:ConsultationManager,synthesize:Callable[[tuple[ConsultationResult,...]],Any],
                 execute:Callable[[Any],Any],verify:Callable[[Any,Any],tuple[bool,Any]],
                 learn:Callable[[Any,Any,Any],None]|None=None)->None:
        self.manager,self.synthesize,self.execute,self.verify,self.learn=manager,synthesize,execute,verify,learn

    def run(self,request:ConsultationRequest,*,sources:list[str]|None=None)->ConsultationAttempt:
        results=self.manager.consult_many(request,sources)
        candidate=self.synthesize(results)
        execution=self.execute(candidate)
        verified,evidence=self.verify(candidate,execution)
        if self.learn and verified:
            self.learn(candidate,execution,evidence)
        return ConsultationAttempt(results,candidate,execution,verified,evidence)
