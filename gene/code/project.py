"""Project representation and filesystem discovery for code-aware work."""
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

    def contains(self, path: Path) -> bool:
        try:
            path.resolve().relative_to(self.root)
            return True
        except ValueError:
            return False

    def relative(self, path: Path) -> Path:
        resolved = path.resolve()
        if not self.contains(resolved):
            raise ValueError(f"path is outside project: {path}")
        return resolved.relative_to(self.root)

    def files(self, *, suffixes: set[str] | None = None) -> tuple[Path, ...]:
        found: list[Path] = []
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in path.parts):
                continue
            if suffixes is not None and path.suffix not in suffixes:
                continue
            found.append(path)
        return tuple(sorted(found))
