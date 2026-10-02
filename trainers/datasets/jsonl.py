"""Streaming JSON Lines dataset adapter."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Iterator
from .base import Sample

class JsonlDataset:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def __iter__(self) -> Iterator[Sample]:
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                item = json.loads(line)
                yield Sample(item.get("input"), item.get("target"), dict(item.get("metadata", {})))

    def __len__(self) -> int:
        with self.path.open("r", encoding="utf-8") as handle:
            return sum(bool(line.strip()) for line in handle)
