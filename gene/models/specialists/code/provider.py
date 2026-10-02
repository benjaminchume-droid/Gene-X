from gene.models.specialists.base import Specialist
class CodeSpecialist(Specialist):
    name="code"
    def __init__(self,handler):self.handler=handler
    def capabilities(self):return {"code"}
    def invoke(self,capability,input,**kwargs):return self.handler(input,**kwargs)
