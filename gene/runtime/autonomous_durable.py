"""Durable autonomous execution with checkpoint-before/after semantics."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from typing import Callable
from .cognitive import CognitiveRuntime, ExecutionRecord
from .persistence import RuntimePersistence

@dataclass(frozen=True, slots=True)
class DurableRun:
    cycles:int
    completed:int
    failed:int
    elapsed_seconds:float
    stopped:bool
    checkpoint:str

class DurableAutonomousDriver:
    def __init__(self,runtime:CognitiveRuntime,persistence:RuntimePersistence,checkpoint_path:str,*,on_cycle:Callable[[tuple[ExecutionRecord,...]],None]|None=None)->None:
        self.runtime=runtime; self.persistence=persistence; self.checkpoint_path=checkpoint_path; self.on_cycle=on_cycle
    def checkpoint(self)->None:
        self.persistence.save(self.runtime,self.checkpoint_path)
    def run(self,*,max_cycles:int|None=None,max_seconds:float|None=None)->DurableRun:
        if max_cycles is not None and max_cycles<0: raise ValueError("max_cycles cannot be negative")
        started=monotonic(); cycles=completed=failed=0
        self.checkpoint()
        while self.runtime.ready():
            if max_cycles is not None and cycles>=max_cycles: break
            if max_seconds is not None and monotonic()-started>=max_seconds: break
            records=self.runtime.run_ready()
            cycles+=1; completed+=sum(r.status.value=="succeeded" for r in records); failed+=sum(r.status.value=="failed" for r in records)
            self.checkpoint()
            if self.on_cycle:self.on_cycle(records)
        stopped=bool(self.runtime.ready())
        return DurableRun(cycles,completed,failed,monotonic()-started,stopped,self.checkpoint_path)
