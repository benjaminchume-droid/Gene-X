"""Source-file representation with stable identity and edits."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

@dataclass(frozen=True)
class SourceFile:
    path: Path
    content: str

    @property
    def suffix(self) -> str:
        return self.path.suffix

    @property
    def digest(self) -> str:
        return sha256(self.content.encode("utf-8")).hexdigest()

    def replace(self, old: str, new: str, *, count: int = -1) -> "SourceFile":
        if count == 0:
            return self
        if old not in self.content:
            raise ValueError("text to replace was not found")
        return SourceFile(self.path, self.content.replace(old, new, count))

    def write(self, root: Path) -> Path:
        target = (root / self.path).resolve() if not self.path.is_absolute() else self.path.resolve()
        root_resolved = root.resolve()
        try:
            target.relative_to(root_resolved)
        except ValueError as exc:
            raise ValueError("source path escapes workspace") from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.content, encoding="utf-8")
        return target
