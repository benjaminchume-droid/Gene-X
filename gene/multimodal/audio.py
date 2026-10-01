"""Audio representation boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class AudioSignal:
    samples: Any
    sample_rate: int
    channels: int = 1

    def __post_init__(self) -> None:
        if self.sample_rate <= 0 or self.channels <= 0:
            raise ValueError("invalid audio format")
