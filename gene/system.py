"""Composition root for the complete Gene organism."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from gene.interface import Gene, GeneResponse
from gene.consultation.manager import ConsultationManager, ConsultationRequest, ConsultationResult
from gene.tools.registry import Tool, ToolRegistry
from gene.capabilities.capability import Capability
from gene.runtime.learning_loop import LearningLoop
from gene.learning.signals import LearningSignal
from gene.evaluation.suite import EvaluationSuite, EvaluationReport
from gene.brain.context import ContextStore
from gene.substrate.ontology import WorldModel
from gene.multimodal.encoders import TrainableEncoder
from gene.multimodal.fusion_learning import LearnedFusion
from gene.generation.engines import TextEngine, ImageEngine, AudioEngine, MusicEngine, VideoEngine, WorldEngine
from gene.perception.pipeline import PerceptionPipeline, Observation
from gene.security.policy import Policy
from gene.learning.organism import LearningOrganism
from gene.training.organism import GeneTrainingSession

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
    perception: PerceptionPipeline = field(default_factory=PerceptionPipeline)
    security: Policy = field(default_factory=Policy)
    chat_backend: Callable[[Any], str] | None = None
    learner: LearningOrganism = field(default_factory=LearningOrganism)
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

    def __post_init__(self) -> None:
        # Connect execution learning to the same organism used by objectives.
        self.organism.runtime.attach_learning(
            LearningLoop(self.learner, lambda _input, outcome: (
                LearningSignal(kind="outcome", value=1.0 if isinstance(outcome, dict) and outcome.get("status") == "succeeded" else 0.0, source="runtime"),
            ))
        )


    def training_session(self, teachers=()):
        return GeneTrainingSession(self.learner, memory=self.organism.memory, teachers=teachers)

    def register_chat_backend(self, backend: Callable[[Any], str]) -> None:
        self.chat_backend = backend

    def chat(self, input_value: Any, *, complexity: float = 2.0) -> GeneResponse:
        if self.chat_backend is None:
            raise RuntimeError("no language generation backend is registered")
        return self.think(
            input_value,
            complexity=complexity,
            interpret=lambda value: self.kernel.observe_language(str(value))[0],
            reason=lambda representation, retrieved: representation,
            act=self.chat_backend,
        )

    def perceive(self, modality: str, input_data: Any, *, context: Any = None) -> Observation:
        return self.perception.perceive(modality, input_data, context=context)

    def register_tool(self, tool: Tool) -> None:
        self.tools.register(tool)
        self.kernel.capabilities.register(Capability(
            name=f"tool:{tool.name}",
            description=tool.description,
            invoke=lambda arguments, _tool=tool: _tool.execute(**arguments) if isinstance(arguments, dict) else _tool.execute(arguments),
            permissions=tool.capabilities,
            source="tool",
        ))

    def execute_tool(self, name: str, arguments: Any = None) -> Any:
        tool = self.tools.get(name)
        for capability in tool.capabilities:
            self.security.require(capability)
        return tool.execute(**arguments) if isinstance(arguments, dict) else tool.execute(arguments)

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
            "perception_providers": tuple(self.perception.providers),
            "security_allowed": tuple(sorted(self.security.allowed)),
            "objectives": len(self.organism.runtime.objectives.objectives),
            "memory_records": len(tuple(self.organism.memory.records())),
            "evaluation_cases": len(self.evaluation.cases),
        }

__all__=["GeneSystem","GeneCapabilities"]
