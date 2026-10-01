"""Registry for executable tools with explicit capability boundaries."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(frozen=True)
class Tool:
    name: str
    execute: Callable[..., Any]
    description: str = ""
    capabilities: frozenset[str] = field(default_factory=frozenset)

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def find(self, capability: str) -> list[Tool]:
        return [tool for tool in self._tools.values() if tool.supports(capability)]

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)
