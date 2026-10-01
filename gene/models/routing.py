"""Capability routing based on requirements and resource constraints."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .interface import CapabilityProvider
from .registry import ModelRegistry

@dataclass(frozen=True)
class ResourceBudget:
    memory_mb: int | None = None
    cpu_threads: int | None = None
    gpu_required: bool = False

@dataclass(frozen=True)
class CapabilityRequest:
    capability: str
    input: Any = None
    preferred_provider: str | None = None
    budget: ResourceBudget = field(default_factory=ResourceBudget)
    metadata: dict[str, Any] = field(default_factory=dict)

class CapabilityRouter:
    def __init__(self, registry: ModelRegistry) -> None:
        self.registry = registry

    def candidates(self, request: CapabilityRequest) -> list[CapabilityProvider]:
        providers = self.registry.providers_for(request.capability)
        if request.preferred_provider:
            preferred = [p for p in providers if p.name == request.preferred_provider]
            others = [p for p in providers if p.name != request.preferred_provider]
            return preferred + others
        return providers

    def invoke(self, request: CapabilityRequest, **kwargs: Any) -> Any:
        candidates = self.candidates(request)
        if not candidates:
            raise LookupError(f"no provider for capability: {request.capability}")
        last_error: Exception | None = None
        for provider in candidates:
            try:
                return provider.invoke(request.capability, request.input, **kwargs)
            except (NotImplementedError, LookupError) as exc:
                last_error = exc
        raise RuntimeError(f"no candidate could execute {request.capability}") from last_error
