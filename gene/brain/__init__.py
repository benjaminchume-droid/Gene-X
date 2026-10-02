"""Hybrid cognitive core for Gene X.

The brain layer combines learned continuous computation with explicit
concept/state/relation structures, bounded working context, and durable
objective state. Language is an interface, not the underlying thought space.
"""
from .model import GeneBrain, BrainOutput
from .representation import FeatureVector, StructuredExample, encode_structure
from .context import ContextBucket, ContextStore
from .training import BrainTrainer, TrainingSample, TrainingReport
from .long_task import LongTaskController, LongTaskState

__all__ = [
    "GeneBrain", "BrainOutput", "FeatureVector", "StructuredExample",
    "encode_structure", "ContextBucket", "ContextStore", "BrainTrainer",
    "TrainingSample", "TrainingReport", "LongTaskController", "LongTaskState",
]
