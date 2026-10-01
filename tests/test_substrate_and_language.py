from gene.substrate.concepts import Concept,ConceptGraph
from gene.substrate.state import StateStore
from gene.language.tokenizer import Tokenizer
from gene.language.interpreter import Interpreter
from gene.language.grounding import Grounder

def test_concept_graph_relation():
 g=ConceptGraph();a=g.add(Concept("program"));b=g.add(Concept("crash"));r=g.relate(a,"has_state",b)
 assert g.related(a,"has_state")==[r]

def test_language_is_grounded_without_tokens_as_state():
 text="Why did my program crash?"
 tokens=Tokenizer().tokenize(text);representation=Interpreter().interpret(text);graph=Grounder().ground(representation)
 assert tokens and representation.intent and representation.intent.kind=="question"
 assert graph.concepts

def test_state_store():
 s=StateStore();s.set("x",42,source="test");assert s.get("x").value==42
