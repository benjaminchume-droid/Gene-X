"""Portable persistence for learned Gene brain state."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .model import GeneBrain


def save_brain(brain: GeneBrain, path: str | Path) -> None:
    data: dict[str, Any] = {
        "version": 1,
        "input_size": brain.input_size,
        "hidden_size": brain.hidden_size,
        "labels": brain.labels,
        "w1": brain.w1,
        "b1": brain.b1,
        "w2": brain.w2,
        "b2": brain.b2,
    }
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")


def load_brain(path: str | Path) -> GeneBrain:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise ValueError("unsupported brain checkpoint version")
    brain = GeneBrain(input_size=int(data["input_size"]), hidden_size=int(data["hidden_size"]))
    brain.labels = [str(x) for x in data["labels"]]
    brain.w1 = [[float(v) for v in row] for row in data["w1"]]
    brain.b1 = [float(v) for v in data["b1"]]
    brain.w2 = [[float(v) for v in row] for row in data["w2"]]
    brain.b2 = [float(v) for v in data["b2"]]
    return brain
