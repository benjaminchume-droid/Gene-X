"""Execution-side filesystem primitives."""
from __future__ import annotations
from pathlib import Path

class Workspace:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, relative: str | Path) -> Path:
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise PermissionError("workspace path escapes root")
        return candidate

    def write(self, relative: str | Path, content: str) -> Path:
        target = self.path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def read(self, relative: str | Path) -> str:
        return self.path(relative).read_text(encoding="utf-8")
