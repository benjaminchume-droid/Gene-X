"""Language-neutral syntax tree boundary."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class SyntaxNode:
    kind: str
    value: Any = None
    children: list["SyntaxNode"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add(self, child: "SyntaxNode") -> None:
        self.children.append(child)
