"""Persistent discourse state for references, focus and conversational grounding."""
from dataclasses import dataclass,field
from typing import Any
from uuid import uuid4
@dataclass(frozen=True)
class DiscourseTurn:
 speaker:str; representation:Any; id:str=field(default_factory=lambda:str(uuid4()))
@dataclass
class DiscourseState:
 turns:list[DiscourseTurn]=field(default_factory=list); focus:Any=None; references:dict[str,Any]=field(default_factory=dict)
 def add(self,speaker,representation):
  turn=DiscourseTurn(speaker,representation);self.turns.append(turn);return turn
 def set_focus(self,focus):self.focus=focus
 def bind(self,name,value):self.references[name]=value
 def resolve(self,name):return self.references.get(name)
