"""Language-neutral syntax tree boundary."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterator

@dataclass
class SyntaxNode:
    kind: str
    value: Any = None
    children: list["SyntaxNode"] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add(self, child: "SyntaxNode") -> "SyntaxNode":
        self.children.append(child)
        return child

    def walk(self) -> Iterator["SyntaxNode"]:
        yield self
        for child in self.children:
            yield from child.walk()

    def find(self, kind: str) -> tuple["SyntaxNode", ...]:
        return tuple(node for node in self.walk() if node.kind == kind)

    def clone(self) -> "SyntaxNode":
        return SyntaxNode(self.kind, self.value, [c.clone() for c in self.children], dict(self.metadata))
