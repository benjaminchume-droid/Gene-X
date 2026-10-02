"""Portable persistence for the adaptive Gene brain."""
from __future__ import annotations

import json
from pathlib import Path
from .model import GeneBrain


def save_brain(brain: GeneBrain, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"version": 2, "brain": brain.state_dict()}, separators=(",", ":")),
        encoding="utf-8",
    )


def load_brain(path: str | Path) -> GeneBrain:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    version = int(data.get("version", 0))
    if version != 2:
        raise ValueError("unsupported brain checkpoint version")
    return GeneBrain.from_state_dict(data["brain"])
