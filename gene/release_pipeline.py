"""Executable release pipeline over build, test, security and artifact checks."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

@dataclass(frozen=True, slots=True)
class ReleaseResult:
    ready:bool
    checks:tuple[tuple[str,bool],...]

class ReleasePipeline:
    def run(self, checks:list[tuple[str,Callable[[],bool]]])->ReleaseResult:
        results=[]
        for name,check in checks:
            try: ok=bool(check())
            except Exception: ok=False
            results.append((name,ok))
        return ReleaseResult(all(ok for _,ok in results),tuple(results))

def filesystem_check(root:str|Path)->Callable[[],bool]:
    path=Path(root)
    return lambda: path.exists() and path.is_dir()
