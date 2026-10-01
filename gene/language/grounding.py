"""Ground linguistic structures into Gene concepts and relations."""
from .representation import LanguageRepresentation
from gene.substrate.concepts import Concept,ConceptGraph
class Grounder:
 def ground(self,representation:LanguageRepresentation)->ConceptGraph:
  graph=ConceptGraph()
  for p in representation.propositions:
   root=graph.add(Concept(p.predicate,attributes={"kind":"predicate"}))
   for name,value in p.arguments.items(): graph.relate(root,name,graph.add(Concept(name,value)),confidence=p.confidence)
  if representation.intent: graph.add(Concept("intent",representation.intent.kind,{"target":representation.intent.target,"parameters":representation.intent.parameters}))
  return graph
