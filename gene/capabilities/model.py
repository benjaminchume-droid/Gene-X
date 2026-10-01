"""Model providers exposed to Gene as capabilities rather than as Gene itself."""
from __future__ import annotations
from typing import Any,Protocol
from .capability import Capability
class ModelProvider(Protocol):
    name:str
    modalities:frozenset[str]
    def invoke(self,request:Any)->Any: ...
class ModelCapability:
    @staticmethod
    def from_provider(provider:ModelProvider)->Capability:
        return Capability(name=f"model:{provider.name}",description=f"Model provider {provider.name}",invoke=lambda args:provider.invoke(args),source="model",metadata if False else {})
