"""Code-generation boundary based on explicit generators."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol

class CodeGenerator(Protocol):
    def generate(self, request: Any) -> str: ...

@dataclass(frozen=True)
class GenerationRequest:
    objective: str
    language: str
    context: Any = None
    constraints: tuple[str, ...] = ()

@dataclass(frozen=True)
class GeneratedSource:
    language: str
    content: str
    metadata: dict[str, Any] | None = None

class GeneratorRegistry:
    def __init__(self) -> None:
        self._generators: dict[str, CodeGenerator] = {}

    def register(self, language: str, generator: CodeGenerator) -> None:
        if language in self._generators:
            raise ValueError(f"generator already registered: {language}")
        self._generators[language] = generator

    def generate(self, request: GenerationRequest) -> GeneratedSource:
        try:
            generator = self._generators[request.language]
        except KeyError as exc:
            raise LookupError(f"no generator for {request.language}") from exc
        return GeneratedSource(request.language, generator.generate(request))
