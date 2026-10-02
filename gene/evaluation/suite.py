"""Capability evaluation without domain-specific knowledge."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
@dataclass(frozen=True,slots=True)
class CaseResult:
    name:str; passed:bool; score:float; detail:Any=None
@dataclass(frozen=True,slots=True)
class EvaluationReport:
    results:tuple[CaseResult,...]; score:float
class EvaluationCase:
    def __init__(self,name:str,run:Callable[[],Any],assess:Callable[[Any],float])->None:self.name,self.run,self.assess=name,run,assess
    def evaluate(self)->CaseResult:
        value=self.run();score=max(0.0,min(1.0,float(self.assess(value))));return CaseResult(self.name,score>=0.5,score,value)
class EvaluationSuite:
    def __init__(self,cases:Iterable[EvaluationCase]=())->None:self.cases=list(cases)
    def add(self,case:EvaluationCase)->None:
        if any(x.name==case.name for x in self.cases):raise ValueError(f"duplicate evaluation case: {case.name}")
        self.cases.append(case)
    def run(self)->EvaluationReport:
        results=tuple(x.evaluate() for x in self.cases);return EvaluationReport(results,sum(x.score for x in results)/len(results) if results else 0.0)
