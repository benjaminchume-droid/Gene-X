"""Skills are executable and verifiable capabilities that can evolve."""
from dataclasses import dataclass,field
from typing import Any,Callable
@dataclass
class Skill:
 name:str; purpose:str; procedure:Callable[[dict[str,Any]],Any]; preconditions:list[Callable[[dict[str,Any]],bool]]=field(default_factory=list); verifier:Callable[[Any,dict[str,Any]],bool]|None=None; metadata:dict[str,Any]=field(default_factory=dict); successes:int=0; failures:int=0
 def applicable(self,state):return all(c(state) for c in self.preconditions)
 def execute(self,state):
  if not self.applicable(state):raise ValueError(f"skill preconditions not satisfied: {self.name}")
  result=self.procedure(state)
  if self.verifier:
   if self.verifier(result,state):self.successes+=1
   else:self.failures+=1
  return result
 @property
 def success_rate(self):
  total=self.successes+self.failures
  return self.successes/total if total else 0.0
