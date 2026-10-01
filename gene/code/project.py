"""Project representation for code-aware work."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Project:
    root: Path
    name: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.root = self.root.resolve()
        if self.name is None:
            self.name = self.root.name
