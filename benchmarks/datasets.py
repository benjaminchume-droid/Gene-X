"""Dataset containers for capability benchmarks.

Benchmark content is supplied externally; this module provides validation,
versioning and reproducible partitioning rather than hard-coded knowledge.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable

@dataclass(frozen=True, slots=True)
class BenchmarkRecord:
    case_id:str
    input:Any
    expected:Any=None
    metadata:dict[str,Any]|None=None

class BenchmarkDataset:
    def __init__(self, records:Iterable[BenchmarkRecord], *, version:str="1"):
        self.version=version; self.records=tuple(records)
        ids=[r.case_id for r in self.records]
        if len(ids)!=len(set(ids)): raise ValueError("duplicate benchmark case id")
    def partition(self,index:int,parts:int)->tuple[BenchmarkRecord,...]:
        if parts<1 or not 0<=index<parts: raise ValueError("invalid partition")
        return tuple(r for i,r in enumerate(self.records) if i%parts==index)
