from gene.models.specialists.base import Specialist
class PlanningSpecialist(Specialist):
    name="planning"
    def __init__(self,handler):self.handler=handler
    def capabilities(self):return {"planning"}
    def invoke(self,capability,input,**kwargs):return self.handler(input,**kwargs)
