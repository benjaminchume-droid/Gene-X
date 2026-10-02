from interfaces.protocols import Interface,Request
class CliApp:
    def __init__(self,interface:Interface): self.interface=interface
    def dispatch(self,operation:str,payload=None): return self.interface.handle(Request(operation,payload))
