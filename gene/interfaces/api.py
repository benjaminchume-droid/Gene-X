"""Framework-neutral API adapter. HTTP frameworks can wrap this handler."""
from .protocol import GeneRequest,ProtocolHandler
class APIHandler:
    def __init__(self,protocol:ProtocolHandler):self.protocol=protocol
    def handle(self,operation,payload):return self.protocol.handle(GeneRequest(operation,payload))
