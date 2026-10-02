"""Domain-neutral world-model inference and consistency checks."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from gene.substrate.ontology import WorldModel, CausalLink

@dataclass(frozen=True, slots=True)
class WorldInference:
    subject:str; property_name:str; value:Any; confidence:float; evidence:tuple[str,...]

class WorldReasoner:
    def __init__(self,world:WorldModel)->None:self.world=world
    def infer_property(self,subject:str,name:str)->WorldInference|None:
        matches=[p for p in self.world.properties if p.subject==subject and p.name==name]
        if not matches:return None
        best=max(matches,key=lambda p:p.confidence)
        return WorldInference(subject,name,best.value,best.confidence,tuple(p.source for p in matches if p.source))
    def causal_candidates(self,cause:str,*,minimum_strength:float=0.0)->tuple[CausalLink,...]:
        return tuple(x for x in self.world.causes if x.cause==cause and x.strength>=minimum_strength)
    def contradictions(self,subject:str,name:str)->tuple[tuple[Any,Any],...]:
        values=[p.value for p in self.world.properties if p.subject==subject and p.name==name]
        return tuple((a,b) for i,a in enumerate(values) for b in values[i+1:] if a!=b)
