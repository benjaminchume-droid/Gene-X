"""Compilation boundary for real toolchains."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Sequence

@dataclass(frozen=True)
class CompilationResult:
    succeeded: bool
    returncode: int
    stdout: str
    stderr: str
    command: tuple[str, ...]

class Compiler:
    def __init__(self, command: str, *, args: Sequence[str] = ()) -> None:
        self.command = command
        self.args = tuple(args)

    def compile(self, target: Path, *, cwd: Path | None = None, timeout: float = 120.0) -> CompilationResult:
        command = (self.command, *self.args, str(target))
        try:
            process = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout)
            return CompilationResult(process.returncode == 0, process.returncode, process.stdout, process.stderr, command)
        except subprocess.TimeoutExpired as exc:
            return CompilationResult(False, -1, exc.stdout or "", exc.stderr or "compilation timed out", command)
