from gene.models.specialists.base import Specialist
class VisionSpecialist(Specialist):
    name="vision"
    def __init__(self,handler):self.handler=handler
    def capabilities(self):return {"vision"}
    def invoke(self,capability,input,**kwargs):return self.handler(input,**kwargs)
