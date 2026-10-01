"""Executable capability with contract and provenance."""
from dataclasses import dataclass,field
from typing import Any,Callable
from uuid import uuid4
@dataclass(frozen=True)
class Capability:
 name:str; description:str; invoke:Callable[[dict[str,Any]],Any]; input_schema:dict[str,Any]=field(default_factory=dict); output_schema:dict[str,Any]=field(default_factory=dict); permissions:frozenset[str]=frozenset(); source:str="native"; id:str=field(default_factory=lambda:str(uuid4()))
 def execute(self,arguments):
  try:return CapabilityResult(self.invoke(arguments),capability_id=self.id)
  except Exception as exc:return CapabilityResult(error=exc,capability_id=self.id)
@dataclass(frozen=True)
class CapabilityResult:
 value:Any=None; error:Exception|None=None; capability_id:str|None=None
 @property
 def succeeded(self):return self.error is None
