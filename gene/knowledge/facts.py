from dataclasses import dataclass,field
from typing import Any
from uuid import uuid4
from .confidence import Confidence
@dataclass(slots=True)
class Fact:
    subject:str; predicate:str; value:Any; confidence:Confidence
    fact_id:str=field(default_factory=lambda:str(uuid4())); evidence_ids:list[str]=field(default_factory=list)
@dataclass
class FactStore:
    facts:dict[str,Fact]=field(default_factory=dict)
    def add(self,fact:Fact)->Fact:self.facts[fact.fact_id]=fact;return fact
    def get(self,fact_id:str)->Fact:return self.facts[fact_id]
    def query(self,subject=None,predicate=None):return tuple(f for f in self.facts.values() if (subject is None or f.subject==subject) and (predicate is None or f.predicate==predicate))
