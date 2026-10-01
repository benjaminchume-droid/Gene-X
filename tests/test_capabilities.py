from gene.capabilities.capability import Capability
from gene.capabilities.registry import CapabilityRegistry
from gene.capabilities.router import CapabilityRequest,CapabilityRouter

def test_capability_registry_and_execution():
 r=CapabilityRegistry();r.register(Capability("echo","Echo",lambda a:a["value"]))
 c=CapabilityRouter(r).resolve(CapabilityRequest("echo"))[0]
 assert c.execute({"value":7}).value==7
