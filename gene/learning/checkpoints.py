"""Portable checkpoint metadata for learned policies, skills and model artifacts."""
from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime,timezone
from typing import Any
@dataclass(frozen=True)
class TrainingCheckpoint:
    artifact_uri:str
    version:str
    metrics:dict[str,float]=field(default_factory=dict)
    parent:str|None=None
    created_at:datetime=field(default_factory=lambda:datetime.now(timezone.utc))
    metadata:dict[str,Any]=field(default_factory=dict)
