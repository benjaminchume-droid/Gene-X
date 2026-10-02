"""Deterministic synchronous parameter aggregation for distributed training."""
from __future__ import annotations
from numbers import Real
from typing import Any

def _average(values:list[Any])->Any:
    first=values[0]
    if isinstance(first,(int,float)):
        return sum(float(v) for v in values)/len(values)
    if isinstance(first,list):
        if not all(isinstance(v,list) and len(v)==len(first) for v in values): raise ValueError("incompatible state shapes")
        return [_average([v[i] for v in values]) for i in range(len(first))]
    if isinstance(first,dict):
        keys=set(first)
        if any(set(v)!=keys for v in values): raise ValueError("incompatible state keys")
        return {k:_average([v[k] for v in values]) for k in keys}
    raise TypeError(f"unsupported trainable state value: {type(first).__name__}")

def average_state_dicts(states:list[dict[str,Any]])->dict[str,Any]:
    if not states: raise ValueError("at least one state is required")
    return _average(states)

class SynchronousAggregator:
    def aggregate(self,states:list[dict[str,Any]])->dict[str,Any]:
        return average_state_dicts(states)
