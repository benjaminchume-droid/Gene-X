from gene.models.specialists.base import Specialist
class ReasoningSpecialist(Specialist):
    name="reasoning"
    def __init__(self,handler):self.handler=handler
    def capabilities(self):return {"reasoning"}
    def invoke(self,capability,input,**kwargs):return self.handler(input,**kwargs)
