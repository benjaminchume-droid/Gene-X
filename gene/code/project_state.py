"""Observable project snapshots used by planning and verification."""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

@dataclass(frozen=True)
class FileState:
    path: Path
    digest: str
    size: int

@dataclass(frozen=True)
class ProjectSnapshot:
    root: Path
    files: tuple[FileState, ...]

    @property
    def digest(self) -> str:
        material = "\n".join(f"{item.path}:{item.digest}:{item.size}" for item in self.files)
        return sha256(material.encode("utf-8")).hexdigest()

def snapshot(root: Path, *, suffixes: set[str] | None = None) -> ProjectSnapshot:
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in path.parts):
            continue
        if suffixes is not None and path.suffix not in suffixes:
            continue
        data = path.read_bytes()
        files.append(FileState(path.relative_to(root), sha256(data).hexdigest(), len(data)))
    return ProjectSnapshot(root.resolve(), tuple(files))
