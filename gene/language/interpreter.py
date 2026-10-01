"""Interpret language into conceptual structures."""
from __future__ import annotations
from typing import Any,Protocol
from .representation import LanguageRepresentation,Intent
class LanguageInterpreterBackend(Protocol):
 def interpret(self,text:str,*,context:Any=None)->LanguageRepresentation: ...
class Interpreter:
 def __init__(self,backend:LanguageInterpreterBackend|None=None): self.backend=backend
 def interpret(self,text:str,*,context:Any=None)->LanguageRepresentation:
  if not text.strip(): raise ValueError("text must not be empty")
  if self.backend:return self.backend.interpret(text,context=context)
  s=text.strip(); return LanguageRepresentation(intent=Intent("question" if s.endswith("?") else "statement",s,confidence=.5),metadata={"raw_text":s,"adapter":"minimal"})
