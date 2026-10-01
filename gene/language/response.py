"""Plan language output from Gene representations before a provider realizes words."""
from dataclasses import dataclass,field
from typing import Any
from .representation import Proposition
@dataclass(frozen=True)
class ResponsePlan:
 propositions:list[Proposition]=field(default_factory=list); purpose:str="answer"; constraints:dict[str,Any]=field(default_factory=dict)
class ResponsePlanner:
 def plan(self,propositions,*,purpose="answer",constraints=None):return ResponsePlan(list(propositions),purpose,constraints or {})
