"""Lifecycle state machine for the Gene runtime."""
from __future__ import annotations
from enum import StrEnum

class Lifecycle(StrEnum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    PAUSING = "pausing"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
