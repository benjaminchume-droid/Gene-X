from gene.runtime.organism import GeneOrganism

def test_gene_organism_arbitration_scopes_execution():
    organism = GeneOrganism()
    selected = organism.create_objective("selected", priority=10)
    deferred = organism.create_objective("deferred", priority=1)
    seen = []
    organism.add_task(selected, lambda: seen.append("selected"))
    organism.add_task(deferred, lambda: seen.append("deferred"))
    observation = organism.observe()
    assert [record.status.value for record in observation.records] == ["succeeded"]
    assert seen == ["selected"]
    assert organism.runtime.objectives.get(deferred.objective_id).status.value == "active"

def test_gene_organism_journals_and_persists_episode_memory():
    organism = GeneOrganism()
    objective = organism.create_objective("durable")
    organism.add_task(objective, lambda: {"value": 3})
    observation = organism.observe()
    assert observation.memories_written == 1
    assert any(entry.event == "task.execution" for entry in organism.journal.entries())
    assert len(tuple(organism.memory.records(kind="episode"))) == 1
    snapshot = organism.snapshot()
    assert snapshot["objectives"][0]["objective_id"] == objective.objective_id
