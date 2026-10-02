"""Atomic checkpoint storage independent of model format."""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

@dataclass(frozen=True, slots=True)
class Checkpoint:
    step: int
    state: dict[str, Any]
    metadata: dict[str, Any]

class CheckpointStore(Protocol):
    def save(self, checkpoint: Checkpoint) -> None: ...
    def load(self, step: int | None = None) -> Checkpoint: ...

class JsonCheckpointStore:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
    def save(self, checkpoint: Checkpoint) -> None:
        target = self.directory / f"checkpoint-{checkpoint.step}.json"
        temp = target.with_suffix(".tmp")
        temp.write_text(json.dumps({
            "step": checkpoint.step,
            "state": checkpoint.state,
            "metadata": checkpoint.metadata,
        }, separators=(",", ":")), encoding="utf-8")
        temp.replace(target)
    def load(self, step: int | None = None) -> Checkpoint:
        files = sorted(self.directory.glob("checkpoint-*.json"))
        if not files:
            raise FileNotFoundError("no checkpoints available")
        target = self.directory / f"checkpoint-{step}.json" if step is not None else files[-1]
        data = json.loads(target.read_text(encoding="utf-8"))
        return Checkpoint(int(data["step"]), dict(data["state"]), dict(data["metadata"]))
