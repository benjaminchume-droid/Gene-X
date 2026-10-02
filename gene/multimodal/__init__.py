"""Multimodal representation and alignment primitives."""
from .fusion import ModalInput, FusedRepresentation, FusionEngine
from .crossmodal import Correspondence
from .alignment import AlignmentSample, AlignmentReport, CrossModalAligner
__all__=["ModalInput","FusedRepresentation","FusionEngine","Correspondence","AlignmentSample","AlignmentReport","CrossModalAligner"]
