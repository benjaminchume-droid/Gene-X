from dataclasses import dataclass
from typing import Callable,Any
@dataclass(frozen=True)
class LoopResult:
    steps:int;stopped:bool;error:Exception|None=None
class RuntimeLoop:
    def __init__(self,step:Callable[[],Any],should_stop:Callable[[Any],bool]):self.step=step;self.should_stop=should_stop
    def run(self,max_steps:int|None=None)->LoopResult:
        count=0
        try:
            while max_steps is None or count<max_steps:
                value=self.step();count+=1
                if self.should_stop(value):return LoopResult(count,True)
            return LoopResult(count,False)
        except Exception as exc:return LoopResult(count,False,exc)
