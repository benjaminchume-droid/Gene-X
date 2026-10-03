"""Unified cognitive scheduler: reflex, conversational and deep execution."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from .latency import CognitiveMode, LatencyController
from .fastpath import FastPathRegistry, OperationSpec, default_fast_path

@dataclass(frozen=True, slots=True)
class Thought:
    mode: CognitiveMode
    input: Any
    interpretation: Any
    retrieved: tuple[Any,...]=()
    inference: Any=None
    action: Any=None
    result: Any=None
    confidence: float=0.0
    elapsed_seconds: float=0.0

@dataclass
class CognitiveScheduler:
    latency: LatencyController=field(default_factory=LatencyController)
    fast_path: FastPathRegistry=field(default_factory=default_fast_path)

    def register_fast_operation(self,name:str,matcher:Callable[[Any],bool],execute:Callable[[Any],Any])->None:
        self.fast_path.register(OperationSpec(name,matcher,execute))

    def run(self, input_value:Any, *, complexity:float=1.0,
            interpret:Callable[[Any],Any]|None=None,
            retrieve:Callable[[Any],tuple[Any,...]]|None=None,
            reason:Callable[[Any,tuple[Any,...]],Any]|None=None,
            act:Callable[[Any],Any]|None=None,
            external_io:bool=False, requires_action:bool=False)->Thought:
        budget=self.latency.classify(complexity=complexity,requires_action=requires_action,requires_external_io=external_io)
        fast=self.fast_path.route(input_value)
        if fast.handled:
            started=self.latency.time(lambda: fast.value,budget.mode)
            return Thought(budget.mode,input_value,input_value,result=started.value,confidence=fast.confidence,elapsed_seconds=started.elapsed_seconds)
        started=self.latency.time(lambda: interpret(input_value) if interpret else input_value,budget.mode)
        interpretation=started.value
        retrieved=retrieve(interpretation) if retrieve else ()
        inference=reason(interpretation,retrieved) if reason else interpretation
        action=act(inference) if act else None
        result=action if action is not None else inference
        return Thought(budget.mode,input_value,interpretation,tuple(retrieved),inference,action,result,1.0,started.elapsed_seconds)
