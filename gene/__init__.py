"""Gene X public API."""
from .interface import Gene, GeneResponse
from .system import GeneSystem, GeneCapabilities
__version__="0.1.0"
__all__=["Gene","GeneResponse","GeneSystem","GeneCapabilities","__version__"]
