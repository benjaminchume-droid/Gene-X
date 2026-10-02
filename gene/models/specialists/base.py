from abc import abstractmethod
from gene.models.interface import CapabilityProvider
class Specialist(CapabilityProvider):
    @abstractmethod
    def capabilities(self)->set[str]:...
