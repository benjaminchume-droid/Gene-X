"""General-purpose source patch primitives."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from .source import SourceFile

@dataclass(frozen=True)
class Patch:
    path: Path
    old: str
    new: str
    count: int = 1

@dataclass(frozen=True)
class PatchResult:
    path: Path
    changed: bool
    before_digest: str
    after_digest: str

class Patcher:
    def apply(self, root: Path, patch: Patch) -> PatchResult:
        target = (root / patch.path).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError as exc:
            raise ValueError("patch path escapes workspace") from exc
        source = SourceFile(patch.path, target.read_text(encoding="utf-8"))
        updated = source.replace(patch.old, patch.new, count=patch.count)
        if updated.digest != source.digest:
            updated.write(root)
        return PatchResult(patch.path, updated.digest != source.digest, source.digest, updated.digest)
