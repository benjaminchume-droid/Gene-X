"""Gene X cognitive kernel connecting language, substrate and capabilities."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
from gene.substrate.state import StateStore
from gene.substrate.concepts import ConceptGraph
from gene.capabilities.registry import CapabilityRegistry
from gene.capabilities.router import CapabilityRouter,CapabilityRequest
from gene.language.interpreter import Interpreter
from gene.language.grounding import Grounder
@dataclass
class CognitiveKernel:
 state:StateStore=field(default_factory=StateStore); concepts:ConceptGraph=field(default_factory=ConceptGraph); capabilities:CapabilityRegistry=field(default_factory=CapabilityRegistry); interpreter:Interpreter=field(default_factory=Interpreter); grounder:Grounder=field(default_factory=Grounder)
 def observe_language(self,text:str,*,source="language"):
  representation=self.interpreter.interpret(text,context=self.state.snapshot()); graph=self.grounder.ground(representation)
  self.state.set("last_language_input",text,source=source); self.state.set("last_language_representation",representation,source=source)
  for c in graph.concepts.values():self.concepts.add(c)
  self.concepts.relations.update(graph.relations)
  return representation,graph
 def capabilities_for(self,purpose,*,permissions=None,names=None):
  return CapabilityRouter(self.capabilities).resolve(CapabilityRequest(purpose,frozenset(permissions or set()),preferred_names=frozenset(names or set())))
 def invoke(self,name,arguments):
  result=self.capabilities.get(name).execute(arguments);self.state.set(f"capability:{name}:last",result,source=name);return result
