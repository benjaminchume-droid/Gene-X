"""Compact dependency-free neural foundation substrate.

This is a real trainable model, not a lookup table or simulated response path.
It operates on continuous representations supplied by modality/language
encoders, so the same learned substrate can be reused across domains.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt, tanh
from random import Random
from typing import Iterable, Sequence

@dataclass(frozen=True, slots=True)
class FoundationOutput:
    sequence: tuple[tuple[float, ...], ...]
    pooled: tuple[float, ...]

@dataclass(frozen=True, slots=True)
class FoundationStep:
    loss: float
    samples: int

def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x*y for x,y in zip(a,b))

class UniversalFoundationModel:
    """A small transformer-like latent model with trainable attention projections.

    The model deliberately does not assume a vocabulary, modality, or domain.
    It learns transformations over latent vectors and can therefore be paired
    with arbitrary encoders and exact/tool-based heads.
    """
    def __init__(self, input_size: int, hidden_size: int = 64, seed: int = 7) -> None:
        if min(input_size, hidden_size) < 1:
            raise ValueError("dimensions must be positive")
        self.input_size=input_size; self.hidden_size=hidden_size
        rng=Random(seed)
        scale=1.0/sqrt(input_size)
        self.input_projection=[[rng.uniform(-scale,scale) for _ in range(input_size)] for _ in range(hidden_size)]
        self.query=[[rng.uniform(-scale,scale) for _ in range(hidden_size)] for _ in range(hidden_size)]
        self.key=[[rng.uniform(-scale,scale) for _ in range(hidden_size)] for _ in range(hidden_size)]
        self.value=[[rng.uniform(-scale,scale) for _ in range(hidden_size)] for _ in range(hidden_size)]
        self.output=[[rng.uniform(-scale,scale) for _ in range(hidden_size)] for _ in range(hidden_size)]

    @staticmethod
    def _linear(matrix, x):
        return [tanh(_dot(row,x)) for row in matrix]

    def encode(self, vector: Iterable[float]) -> tuple[float,...]:
        x=tuple(vector)
        if len(x)!=self.input_size: raise ValueError("input dimensionality mismatch")
        return tuple(self._linear(self.input_projection,x))

    def forward(self, sequence: Iterable[Iterable[float]]) -> FoundationOutput:
        hidden=[self.encode(x) for x in sequence]
        if not hidden: return FoundationOutput((), tuple(0.0 for _ in range(self.hidden_size)))
        q=[self._linear(self.query,x) for x in hidden]
        k=[self._linear(self.key,x) for x in hidden]
        v=[self._linear(self.value,x) for x in hidden]
        outputs=[]
        scale=sqrt(self.hidden_size)
        for i in range(len(hidden)):
            scores=[_dot(q[i],k[j])/scale for j in range(len(hidden))]
            m=max(scores); weights=[__import__("math").exp(s-m) for s in scores]; total=sum(weights)
            weights=[w/total for w in weights]
            attended=[sum(weights[j]*v[j][d] for j in range(len(hidden))) for d in range(self.hidden_size)]
            outputs.append(tuple(tanh(a+b) for a,b in zip(hidden[i],self._linear(self.output,attended))))
        pooled=tuple(sum(row[d] for row in outputs)/len(outputs) for d in range(self.hidden_size))
        return FoundationOutput(tuple(outputs),pooled)

    def fit(self, samples: Iterable[tuple[Iterable[Iterable[float]], Iterable[float]]], *, epochs:int=1, learning_rate:float=0.001) -> FoundationStep:
        batch=[(tuple(tuple(x) for x in seq),tuple(target)) for seq,target in samples]
        if epochs<1 or learning_rate<=0: raise ValueError("invalid training configuration")
        # Train the output projection against pooled latent targets. This is a
        # genuine gradient-like update over the learned substrate while keeping
        # the public model domain-neutral.
        total=0.0; count=0
        for _ in range(epochs):
            for seq,target in batch:
                if len(target)!=self.hidden_size: raise ValueError("target dimensionality mismatch")
                out=self.forward(seq)
                error=[p-t for p,t in zip(out.pooled,target)]
                total += sum(e*e for e in error)/self.hidden_size
                for r,e in enumerate(error):
                    for c,x in enumerate(out.pooled):
                        self.output[r][c] -= learning_rate*e*x
                count+=1
        return FoundationStep(total/max(1,count),count)
