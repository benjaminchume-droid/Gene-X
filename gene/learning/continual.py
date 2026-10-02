from __future__ import annotations
from dataclasses import dataclass
from typing import Callable,Iterable,Any
@dataclass(frozen=True)
class ContinualStep:
    sample:Any; loss:float
class ContinualLearner:
    def __init__(self,update:Callable[[Any],float]): self.update=update; self.steps=0
    def learn(self,stream:Iterable[Any])->tuple[ContinualStep,...]:
        out=[]
        for sample in stream:
            loss=float(self.update(sample)); self.steps+=1; out.append(ContinualStep(sample,loss))
        return tuple(out)
