from gene.models.specialists.base import Specialist
class LanguageSpecialist(Specialist):
    name="language"
    def __init__(self,handler):self.handler=handler
    def capabilities(self):return {"language"}
    def invoke(self,capability,input,**kwargs):return self.handler(input,**kwargs)
