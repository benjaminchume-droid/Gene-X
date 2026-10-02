"""Long-running autonomous driver for the durable cognitive runtime."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic
from typing import Callable
from .cognitive import CognitiveRuntime, ExecutionRecord

@dataclass(frozen=True,slots=True)
class AutonomousRun:
    cycles:int
    completed:int
    failed:int
    elapsed_seconds:float
    stopped:bool

class AutonomousDriver:
    def __init__(self,runtime:CognitiveRuntime,*,on_cycle:Callable[[tuple[ExecutionRecord,...]],None]|None=None)->None:
        self.runtime=runtime; self.on_cycle=on_cycle

    def run(self,*,max_cycles:int|None=None,max_seconds:float|None=None)->AutonomousRun:
        if max_cycles is not None and max_cycles<0: raise ValueError("max_cycles cannot be negative")
        if max_seconds is not None and max_seconds<=0: raise ValueError("max_seconds must be positive")
        started=monotonic(); cycles=completed=failed=0
        while self.runtime.ready():
            if max_cycles is not None and cycles>=max_cycles: break
            if max_seconds is not None and monotonic()-started>=max_seconds: break
            records=self.runtime.run_ready(); cycles+=1
            completed+=sum(x.status.value=="succeeded" for x in records)
            failed+=sum(x.status.value=="failed" for x in records)
            if self.on_cycle:self.on_cycle(records)
        return AutonomousRun(cycles,completed,failed,monotonic()-started,bool(self.runtime.ready()))
