"""Provider registry, routing, and optional resource-aware loading."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .interface import CapabilityProvider
from .loading import ProviderLoader

@dataclass(frozen=True, slots=True)
class ModelRoute:
    provider: str
    capability: str

class ModelRegistry:
    def __init__(self, loader: ProviderLoader | None = None) -> None:
        self.loader=loader
        self._providers: dict[str,CapabilityProvider]={}

    def register(self,provider:CapabilityProvider)->None:
        if provider.name in self._providers: raise ValueError(f"provider already registered: {provider.name}")
        self._providers[provider.name]=provider

    def get(self,name:str)->CapabilityProvider:return self._providers[name]

    def providers_for(self,capability:str)->list[CapabilityProvider]:
        return [p for p in self._providers.values() if capability in p.capabilities()]

    def route(self,capability:str,preferred:str|None=None)->CapabilityProvider:
        if preferred is not None:
            provider=self._providers.get(preferred)
            if provider is not None and capability in provider.capabilities(): return provider
        candidates=self.providers_for(capability)
        if not candidates: raise LookupError(f"no provider for capability: {capability}")
        return candidates[0]

    def invoke(self,capability:str,input:Any,*,preferred:str|None=None,load:bool=True,**kwargs:Any)->Any:
        provider=self.route(capability,preferred)
        if load and self.loader is not None: self.loader.load(provider)
        return provider.invoke(capability,input,**kwargs)
