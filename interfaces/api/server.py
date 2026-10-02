from interfaces.protocols import Interface,Request,Response
class ApiServer:
    def __init__(self,handler:Interface): self.handler=handler
    def handle(self,request:Request)->Response: return self.handler.handle(request)
