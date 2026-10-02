from gene.generation.base import Generator
class ImageGenerator(Generator):
    def __init__(self,engine): self.engine=engine
    def generate(self,request): return self.engine.generate(request)
