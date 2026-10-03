"""Capability-growth evaluation independent of model size or context length."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable,Any

@dataclass(frozen=True, slots=True)
class CapabilityCase:
    case_id:str
    input:Any
    expected:Any
    evaluator:Callable[[Any,Any],float]

@dataclass(frozen=True, slots=True)
class CapabilityReport:
    scores:dict[str,float]
    mean:float

class CapabilityBenchmark:
    def run(self, cases:list[CapabilityCase], system:Callable[[Any],Any])->CapabilityReport:
        scores={case.case_id:float(case.evaluator(system(case.input),case.expected)) for case in cases}
        return CapabilityReport(scores,sum(scores.values())/len(scores) if scores else 0.0)
