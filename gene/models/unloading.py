"""Explicit and policy-driven unloading of loaded providers."""
from __future__ import annotations
from typing import Any
from .loading import ProviderLoader, Loadable

class ProviderUnloader:
    def __init__(self, loader: ProviderLoader) -> None:
        self.loader = loader

    def unload(self, provider: Loadable) -> None:
        self.loader.unload(provider)

    def unload_until(self, providers: list[Loadable], required_memory_mb: int) -> list[str]:
        freed: list[str] = []
        for provider in providers:
            if self.loader.ledger.memory_used_mb <= required_memory_mb:
                break
            self.unload(provider)
            freed.append(provider.name)
        return freed
