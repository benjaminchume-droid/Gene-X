"""Capability routing by declared affordances."""
from dataclasses import dataclass
@dataclass(frozen=True)
class CapabilityRequest:
 purpose:str; required_permissions:frozenset[str]=frozenset(); preferred_source:str|None=None; preferred_names:frozenset[str]=frozenset()
class CapabilityRouter:
 def __init__(self,registry):self.registry=registry
 def resolve(self,request):
  xs=self.registry.find(permissions=set(request.required_permissions),source=request.preferred_source)
  if request.preferred_names:return [c for c in xs if c.name in request.preferred_names]+[c for c in xs if c.name not in request.preferred_names]
  return xs
