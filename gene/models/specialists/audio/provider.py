from gene.models.specialists.base import Specialist
class AudioSpecialist(Specialist):
    name="audio"
    def __init__(self,handler):self.handler=handler
    def capabilities(self):return {"audio"}
    def invoke(self,capability,input,**kwargs):return self.handler(input,**kwargs)
