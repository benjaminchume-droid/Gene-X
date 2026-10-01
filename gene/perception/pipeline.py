"""Provider-independent multimodal perception."""
from dataclasses import dataclass,field
from typing import Any,Protocol
from datetime import datetime,timezone
from uuid import uuid4
@dataclass(frozen=True)
class Observation:
 modality:str; representation:Any; source:str; confidence:float=1.0; id:str=field(default_factory=lambda:str(uuid4())); observed_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
class PerceptionProvider(Protocol):
 modality:str
 def perceive(self,input_data:Any,*,context:Any=None)->Any: ...
class PerceptionPipeline:
 def __init__(self):self.providers={}
 def register(self,provider):self.providers[provider.modality]=provider
 def perceive(self,modality,input_data,*,context=None):
  p=self.providers.get(modality)
  if p is None:raise KeyError(f"no perception provider for modality: {modality}")
  return Observation(modality,p.perceive(input_data,context=context),type(p).__name__)
