"""Provider-independent multimodal expression."""
from dataclasses import dataclass
from typing import Any,Protocol
@dataclass(frozen=True)
class ExpressionRequest:modality:str;representation:Any;constraints:dict[str,Any]|None=None
@dataclass(frozen=True)
class ExpressionResult:modality:str;value:Any;provider:str
class ExpressionProvider(Protocol):
 modality:str
 def express(self,representation:Any,*,constraints:dict[str,Any]|None=None)->Any: ...
class ExpressionPipeline:
 def __init__(self):self.providers={}
 def register(self,provider):self.providers[provider.modality]=provider
 def express(self,request):
  p=self.providers.get(request.modality)
  if p is None:raise KeyError(f"no expression provider for modality: {request.modality}")
  return ExpressionResult(request.modality,p.express(request.representation,constraints=request.constraints),type(p).__name__)
