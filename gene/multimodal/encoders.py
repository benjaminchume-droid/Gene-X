"""Trainable modality encoders.

Encoders normalize heterogeneous observations into Gene's shared latent space.
They accept supplied numeric samples and learn through reconstruction targets;
there are no modality-specific semantic labels or baked-in objects.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import tanh
from random import Random
from typing import Iterable, Sequence

@dataclass(frozen=True, slots=True)
class EncoderStep:
    loss: float
    samples: int

class TrainableEncoder:
    def __init__(self,input_size:int,latent_size:int=64,seed:int=7)->None:
        if min(input_size,latent_size)<1: raise ValueError("dimensions must be positive")
        self.input_size=input_size; self.latent_size=latent_size
        rng=Random(seed); scale=1.0/max(1,input_size)**0.5
        self.weights=[[rng.uniform(-scale,scale) for _ in range(input_size)] for _ in range(latent_size)]
        self.bias=[0.0]*latent_size

    def encode(self,values:Iterable[float])->tuple[float,...]:
        x=tuple(values)
        if len(x)!=self.input_size: raise ValueError("input dimensionality mismatch")
        return tuple(tanh(sum(w*v for w,v in zip(row,x))+b) for row,b in zip(self.weights,self.bias))

    def fit(self,samples:Iterable[tuple[Iterable[float],Iterable[float]]],*,epochs:int=1,learning_rate:float=.01)->EncoderStep:
        batch=[(tuple(x),tuple(t)) for x,t in samples]
        if epochs<1 or learning_rate<=0: raise ValueError("invalid training configuration")
        total=0.0; count=0
        for _ in range(epochs):
            for x,target in batch:
                if len(x)!=self.input_size or len(target)!=self.latent_size: raise ValueError("sample dimensionality mismatch")
                pred=self.encode(x); errors=[p-t for p,t in zip(pred,target)]
                total += sum(e*e for e in errors)/self.latent_size
                for i,e in enumerate(errors):
                    grad=2*e*(1-pred[i]*pred[i])
                    for j,v in enumerate(x): self.weights[i][j]-=learning_rate*grad*v
                    self.bias[i]-=learning_rate*grad
                count+=1
        return EncoderStep(total/max(1,count),count)

class ImageEncoder(TrainableEncoder):
    pass

class AudioEncoder(TrainableEncoder):
    def __init__(self, input_size=None, latent_size=64, seed=7):
        super().__init__(input_size or 1, latent_size, seed)
    def encode(self, values, *args):
        if args:
            flat=tuple(float(v) for v in values)
            return EncodedSignal((sum(flat),min(flat) if flat else 0.0,max(flat) if flat else 0.0,sum(v*v for v in flat),float(len(flat))),(len(flat),))
        return super().encode(values)

class VideoEncoder(TrainableEncoder):
    def __init__(self, input_size=None, latent_size=64, seed=7):
        super().__init__(input_size or 1, latent_size, seed)
    def encode(self, values, *args):
        if args:
            flat=[]
            def visit(node):
                if isinstance(node,(list,tuple)):
                    for item in node: visit(item)
                else: flat.append(float(node))
            visit(values)
            return EncodedSignal((float(len(flat)),sum(flat),min(flat) if flat else 0.0,max(flat) if flat else 0.0,sum(v*v for v in flat)),(len(flat),))
        return super().encode(values)

class SpatialEncoder(TrainableEncoder):
    def __init__(self, input_size=None, latent_size=64, seed=7):
        super().__init__(input_size or 1, latent_size, seed)
    def encode(self, values, *args):
        if args:
            rows=[tuple(float(x) for x in row) for row in values]
            return EncodedSignal(tuple(x for row in rows for x in row),(len(rows),len(rows[0]) if rows else 0))
        return super().encode(values)


@dataclass(frozen=True, slots=True)
class EncodedSignal:
    vector: tuple[float, ...]
    shape: tuple[int, ...] = ()

class NumericImageEncoder:
    def encode(self, value):
        flat=[]
        shape=[]
        def visit(node, depth=0):
            if isinstance(node,(list,tuple)):
                if len(shape)<=depth: shape.append(len(node))
                for item in node: visit(item,depth+1)
            else: flat.append(float(node))
        visit(value)
        return EncodedSignal(tuple(flat),tuple(shape))

class _SummaryEncoder:
    def encode(self, value, *args):
        flat=[]
        def visit(node):
            if isinstance(node,(list,tuple)):
                for item in node: visit(item)
            else: flat.append(float(node))
        visit(value)
        return EncodedSignal((sum(flat),min(flat) if flat else 0.0,max(flat) if flat else 0.0,sum(x*x for x in flat),float(len(flat))),(len(flat),))

class LegacySpatialEncoder:
    def encode(self, value):
        rows=[tuple(float(x) for x in row) for row in value]
        return EncodedSignal(tuple(x for row in rows for x in row),(len(rows),len(rows[0]) if rows else 0))

NumericAudioEncoder=_SummaryEncoder
NumericVideoEncoder=_SummaryEncoder
NumericSpatialEncoder=LegacySpatialEncoder
