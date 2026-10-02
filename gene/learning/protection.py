"""Continual-learning protection using replay and bounded updates."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from .replay import ReplayBuffer

@dataclass(frozen=True, slots=True)
class LearningStep:
    sample: Any
    loss: float

@dataclass(frozen=True, slots=True)
class LearningReport:
    steps: tuple[LearningStep, ...]
    replayed: int
    mean_loss: float

class ProtectedLearner:
    def __init__(self, update: Callable[[Any], float], *, replay: ReplayBuffer | None = None, replay_ratio: float = 0.25) -> None:
        if not 0.0 <= replay_ratio <= 1.0: raise ValueError("replay_ratio must be between 0 and 1")
        self.update,self.replay,self.replay_ratio=update,replay or ReplayBuffer(),replay_ratio
    def learn(self, stream: Iterable[Any]) -> LearningReport:
        steps=[]; replayed=0
        for sample in stream:
            loss=float(self.update(sample)); steps.append(LearningStep(sample,loss)); self.replay.add(sample)
            for old in self.replay.sample(int(len(self.replay)*self.replay_ratio)):
                if old is sample: continue
                self.update(old); replayed+=1
        return LearningReport(tuple(steps),replayed,sum(x.loss for x in steps)/len(steps) if steps else 0.0)
