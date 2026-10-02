"""Distributed training primitives using explicit dataset sharding.

The coordinator is backend-neutral. A process/thread/cluster executor can be
injected; no fake remote workers are hidden here.
"""
from __future__ import annotations
from dataclasses import dataclass
from concurrent.futures import Executor, Future
from typing import Callable, Iterable, TypeVar

T=TypeVar("T"); R=TypeVar("R")
@dataclass(frozen=True, slots=True)
class WorkerSpec:
    rank:int
    world_size:int

@dataclass(frozen=True, slots=True)
class DistributedResult:
    results: tuple[R,...]
    world_size:int

class DistributedTrainer:
    def __init__(self, executor:Executor|None=None) -> None: self.executor=executor
    def run(self, records:Iterable[T], worker:Callable[[WorkerSpec,list[T]],R], *, world_size:int=1)->DistributedResult:
        if world_size<1: raise ValueError("world_size must be positive")
        items=list(records)
        shards=[items[r::world_size] for r in range(world_size)]
        if self.executor is None:
            results=tuple(worker(WorkerSpec(r,world_size),shards[r]) for r in range(world_size))
        else:
            futures: list[Future[R]]=[self.executor.submit(worker,WorkerSpec(r,world_size),shards[r]) for r in range(world_size)]
            results=tuple(f.result() for f in futures)
        return DistributedResult(results,world_size)
