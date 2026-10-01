"""Source-file representation."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class SourceFile:
    path: Path
    content: str

    @property
    def suffix(self) -> str:
        return self.path.suffix
