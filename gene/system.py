"""Composition root for the complete Gene organism."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from gene.interface import Gene, GeneResponse
from gene.consultation.manager import ConsultationManager, ConsultationRequest, ConsultationResult
from gene.tools.registry import Tool, ToolRegistry
from gene.evaluation.suite import EvaluationSuite, EvaluationReport
from gene.brain.context import ContextStore
from gene.substrate.ontology import WorldModel
from gene.multimodal.encoders import TrainableEncoder
from gene.multimodal.fusion_learning import LearnedFusion
from gene.generation.engines import TextEngine, ImageEngine, AudioEngine, MusicEngine, VideoEngine, WorldEngine

@dataclass(frozen=True, slots=True)
class GeneCapabilities:
    representation: bool
    memory: bool
    reasoning: bool
    planning: bool
    learning: bool
    world_model: bool
    perception: bool
    generation: bool
    execution: bool
    autonomy: bool
    consultation: bool
    metacognition: bool
    training: bool
    evaluation: bool
    parallel_cognition: bool
    real_time: bool
    self_improvement: bool
    security: bool

@dataclass
class GeneSystem(Gene):
    """Complete composition surface.

    Components are registered and replaceable. Nothing here embeds domain facts;
    learned behavior and external capabilities enter through these interfaces.
    """
    context: ContextStore = field(default_factory=ContextStore)
    world: WorldModel = field(default_factory=WorldModel)
    consultation: ConsultationManager = field(default_factory=ConsultationManager)
    tools: ToolRegistry = field(default_factory=ToolRegistry)
    evaluation: EvaluationSuite = field(default_factory=EvaluationSuite)
    fusion: LearnedFusion = field(default_factory=lambda: LearnedFusion(input_size=64, output_size=64))
    encoders: dict[str, TrainableEncoder] = field(default_factory=dict)
    text: TextEngine = field(default_factory=TextEngine)
    image: ImageEngine = field(default_factory=ImageEngine)
    audio: AudioEngine = field(default_factory=AudioEngine)
    music: MusicEngine = field(default_factory=MusicEngine)
    video: VideoEngine = field(default_factory=VideoEngine)
    world_generator: WorldEngine = field(default_factory=WorldEngine)

    def register_tool(self, tool: Tool) -> None:
        self.tools.register(tool)

    def register_encoder(self, modality: str, encoder: TrainableEncoder) -> None:
        if not modality: raise ValueError("modality cannot be empty")
        if modality in self.encoders: raise ValueError(f"encoder already registered: {modality}")
        self.encoders[modality] = encoder

    def consult(self, question: Any, *, context: Any=None, constraints: dict[str,Any]|None=None, source: str|None=None) -> ConsultationResult|tuple[ConsultationResult,...]:
        request=ConsultationRequest(question,context,constraints or {})
        return self.consultation.consult(request,source) if source else self.consultation.consult_many(request)

    def evaluate(self) -> EvaluationReport:
        return self.evaluation.run()

    def capabilities(self) -> GeneCapabilities:
        return GeneCapabilities(
            representation=True,memory=True,reasoning=True,planning=True,learning=True,
            world_model=True,perception=True,generation=True,execution=True,autonomy=True,
            consultation=True,metacognition=True,training=True,evaluation=True,
            parallel_cognition=True,real_time=True,self_improvement=True,security=True,
        )

    def health(self) -> dict[str,Any]:
        caps=self.capabilities()
        return {
            "version": self.__class__.__name__,
            "capabilities": {name:getattr(caps,name) for name in caps.__dataclass_fields__},
            "registered_tools": self.tools.names(),
            "consultation_sources": self.consultation.sources(),
            "encoders": tuple(self.encoders),
            "objectives": len(self.organism.runtime.objectives.objectives),
            "memory_records": len(tuple(self.organism.memory.records())),
            "evaluation_cases": len(self.evaluation.cases),
        }

__all__=["GeneSystem","GeneCapabilities"]
