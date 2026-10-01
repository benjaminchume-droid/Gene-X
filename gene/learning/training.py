"""Training orchestration primitives independent of a particular ML framework."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any,Callable
from .environment import TrainingEnvironment,Episode
@dataclass(frozen=True)
class TrainingExample:
    observation:Any
    action:Any
    outcome:Any
    score:float
@dataclass
class TrainingRun:
    episodes:list[Episode]=field(default_factory=list)
    examples:list[TrainingExample]=field(default_factory=list)
    metadata:dict[str,Any]=field(default_factory=dict)
class Trainer:
    def __init__(self,policy:Callable[[Any],Any]):self.policy=policy
    def run_episode(self,environment:TrainingEnvironment,*,seed:int|None=None,max_steps:int=100)->Episode:
        state=environment.reset(seed=seed);episode=Episode()
        for _ in range(max_steps):
            action=self.policy(state)
            step=environment.step(action);episode.add(step)
            state=step.observation
            if step.done:break
        return episode
