"""Training environments expose real tasks and measurable outcomes to Gene."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any,Protocol
from uuid import uuid4
@dataclass(frozen=True)
class EnvironmentState:
    values:dict[str,Any]=field(default_factory=dict)
@dataclass(frozen=True)
class EnvironmentStep:
    observation:Any
    reward:float=0.0
    done:bool=False
    info:dict[str,Any]=field(default_factory=dict)
class TrainingEnvironment(Protocol):
    def reset(self, seed:int|None=None)->EnvironmentState: ...
    def step(self, action:Any)->EnvironmentStep: ...
    def evaluate(self, result:Any)->float: ...
@dataclass
class Episode:
    id:str=field(default_factory=lambda:str(uuid4()))
    steps:list[EnvironmentStep]=field(default_factory=list)
    total_reward:float=0.0
    completed:bool=False
    def add(self,step:EnvironmentStep)->None:
        self.steps.append(step);self.total_reward+=step.reward;self.completed=step.done
