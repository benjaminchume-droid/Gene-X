"""Trainable cross-modal fusion over encoder outputs."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from random import Random
from typing import Sequence

@dataclass(frozen=True, slots=True)
class FusionStep:
    loss: float
    samples: int

class LearnedFusion:
    def __init__(self, input_size:int, output_size:int, seed:int=11) -> None:
        if input_size<1 or output_size<1: raise ValueError("dimensions must be positive")
        self.input_size=input_size; self.output_size=output_size
        r=Random(seed); s=1/sqrt(input_size)
        self.weights=[[r.uniform(-s,s) for _ in range(input_size)] for _ in range(output_size)]
        self.bias=[0.0]*output_size

    def forward(self, vectors:Sequence[Sequence[float]])->tuple[float,...]:
        if not vectors: return tuple(self.bias)
        x=[sum(v[d] for v in vectors)/len(vectors) for d in range(len(vectors[0]))]
        if len(x)!=self.input_size: raise ValueError("fusion dimensionality mismatch")
        return tuple(sum(w*x[d] for d,w in enumerate(row))+b for row,b in zip(self.weights,self.bias))

    def fit(self, samples:Sequence[tuple[Sequence[Sequence[float]],Sequence[float]]], *, epochs:int=1, learning_rate:float=.001)->FusionStep:
        total=0.0; count=0
        for _ in range(epochs):
            for vectors,target in samples:
                pred=self.forward(vectors)
                err=[p-t for p,t in zip(pred,target)]
                total+=sum(e*e for e in err)/len(err); count+=1
                x=[sum(v[d] for v in vectors)/len(vectors) for d in range(self.input_size)]
                for o in range(self.output_size):
                    for d in range(self.input_size): self.weights[o][d]-=learning_rate*err[o]*x[d]
                    self.bias[o]-=learning_rate*err[o]
        return FusionStep(total/max(count,1),count)

    def state_dict(self)->dict:
        return {"input_size":self.input_size,"output_size":self.output_size,"weights":[r[:] for r in self.weights],"bias":self.bias[:]}

    def load_state_dict(self,state:dict)->None:
        if (state["input_size"],state["output_size"])!=(self.input_size,self.output_size): raise ValueError("dimension mismatch")
        self.weights=[list(r) for r in state["weights"]]; self.bias=list(state["bias"])
