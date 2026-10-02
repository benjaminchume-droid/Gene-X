"""Gene X cognitive substrate."""
from .cycle import CognitionCycle, CycleAction, CycleEvaluation, CycleObservation, CycleResult
from .model import BrainOutput, GeneBrain
from .representation import (
    FeatureVector, Representation, RepresentationTrainingReport, StructuredExample,
    TrainableRepresentation, encode_structure,
)
from .context import ContextBucket, ContextStore
from .training import BrainTrainer, RepresentationSample, SimilaritySample, TrainingSample, TrainingReport
from .long_task import LongTaskController, LongTaskState
from .persistence import load_brain, save_brain
from .grounding import GroundedSample, GroundingReport, GroundedRepresentationTrainer
from .predictive import PredictiveCore, PredictionReport

__all__=[
    "BrainOutput","GeneBrain","TrainableRepresentation","FeatureVector","Representation",
    "RepresentationTrainingReport","StructuredExample","encode_structure",
    "CognitionCycle","CycleObservation","CycleAction","CycleEvaluation","CycleResult",
    "ContextBucket","ContextStore","BrainTrainer","TrainingSample","RepresentationSample",
    "SimilaritySample","TrainingReport","LongTaskController","LongTaskState",
    "save_brain","load_brain","GroundedSample","GroundingReport",
    "GroundedRepresentationTrainer","PredictiveCore","PredictionReport",
]
