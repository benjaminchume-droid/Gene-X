"""Provider registry and capability routing foundation."""
from __future__ import annotations
from .interface import CapabilityProvider

class ModelRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, CapabilityProvider] = {}

    def register(self, provider: CapabilityProvider) -> None:
        if provider.name in self._providers:
            raise ValueError(f"provider already registered: {provider.name}")
        self._providers[provider.name] = provider

    def get(self, name: str) -> CapabilityProvider:
        return self._providers[name]

    def providers_for(self, capability: str) -> list[CapabilityProvider]:
        return [p for p in self._providers.values() if capability in p.capabilities()]
