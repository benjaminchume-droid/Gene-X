"""Release manifest generation from repository and verification state."""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
from pathlib import Path

@dataclass(frozen=True,slots=True)
class ReleaseManifest:
    version:str
    files:int
    digest:str

def build_manifest(root:str|Path,version:str)->ReleaseManifest:
    root=Path(root)
    digest=hashlib.sha256()
    files=0
    for path in sorted(root.rglob("*.py")):
        digest.update(str(path.relative_to(root)).encode())
        digest.update(path.read_bytes())
        files+=1
    return ReleaseManifest(version,files,digest.hexdigest())
