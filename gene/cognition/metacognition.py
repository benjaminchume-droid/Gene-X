"""Learned metacognitive operation selection.

Operations are registered capabilities. Selection starts from neutral priors and
updates from observed outcomes, allowing Gene to learn which cognitive action
works under which structural conditions without embedding domain rules.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from math import exp
from typing import Any, Callable, Iterable

@dataclass(frozen=True, slots=True)
class CognitiveOperation:
    name: str
    execute: Callable[..., Any]

@dataclass(frozen=True, slots=True)
class OperationOutcome:
    operation: str
    context_key: str
    reward: float

@dataclass
class MetacognitiveController:
    operations: dict[str,CognitiveOperation]=field(default_factory=dict)
    values: dict[tuple[str,str],float]=field(default_factory=dict)
    counts: dict[tuple[str,str],int]=field(default_factory=dict)

    def register(self, operation:CognitiveOperation)->None:
        if operation.name in self.operations: raise ValueError(f"operation already registered: {operation.name}")
        self.operations[operation.name]=operation

    def context_key(self, context:Any)->str:
        return repr(context)

    def choose(self, context:Any)->CognitiveOperation:
        if not self.operations: raise LookupError("no cognitive operations registered")
        key=self.context_key(context)
        def score(name:str)->float:
            n=self.counts.get((key,name),0)
            value=self.values.get((key,name),0.0)
            exploration=(1.0/(1+n)**0.5)
            return value+exploration
        return max(self.operations.values(),key=lambda op:score(op.name))

    def learn(self,outcome:OperationOutcome)->None:
        key=(outcome.context_key,outcome.operation)
        n=self.counts.get(key,0)+1
        old=self.values.get(key,0.0)
        self.counts[key]=n
        self.values[key]=old+(outcome.reward-old)/n

    def observe(self,context:Any,operation:str,reward:float)->OperationOutcome:
        outcome=OperationOutcome(operation,self.context_key(context),float(reward))
        self.learn(outcome)
        return outcome
