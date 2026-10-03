"""Public Gene organism interface."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from gene.cognition.kernel import CognitiveKernel
from gene.runtime.cognitive_scheduler import CognitiveScheduler, Thought
from gene.runtime.organism import GeneOrganism

@dataclass(frozen=True, slots=True)
class GeneResponse:
    value: Any
    thought: Thought
    mode: str
    elapsed_seconds: float

@dataclass
class Gene:
    kernel: CognitiveKernel=field(default_factory=CognitiveKernel)
    organism: GeneOrganism=field(default_factory=GeneOrganism)
    scheduler: CognitiveScheduler=field(default_factory=CognitiveScheduler)

    def register_fast_operation(self,name:str,matcher:Callable[[Any],bool],execute:Callable[[Any],Any])->None:
        self.scheduler.register_fast_operation(name,matcher,execute)
    def think(self,input_value:Any,*,complexity:float=1.0,interpret:Callable[[Any],Any]|None=None,
              retrieve:Callable[[Any],tuple[Any,...]]|None=None,reason:Callable[[Any,tuple[Any,...]],Any]|None=None,
              act:Callable[[Any],Any]|None=None,external_io:bool=False,requires_action:bool=False)->GeneResponse:
        thought=self.scheduler.run(input_value,complexity=complexity,interpret=interpret,retrieve=retrieve,reason=reason,act=act,external_io=external_io,requires_action=requires_action)
        return GeneResponse(thought.result,thought,thought.mode.value,thought.elapsed_seconds)
    def objective(self,description:str,**metadata:Any): return self.organism.create_objective(description,**metadata)
    def task(self,objective,operation:Callable[[],Any],**kwargs:Any): return self.organism.add_task(objective,operation,**kwargs)
    def step(self,*,limit:int|None=None): return self.organism.observe(limit=limit)
    def snapshot(self)->dict[str,Any]: return self.organism.snapshot()
