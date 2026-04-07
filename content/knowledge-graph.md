---
title: Knowledge Graph
---

# The LACK Knowledge Graph

The LACK knowledge graph is constructed through a pipeline of relation extraction, entity linking, and Wikidata enrichment, applied to a corpus of investigative journalism sources covering climate lobbying.

---

## KG at a Glance

{{ stats_dashboard }}

---

## Relation Extraction

Relationships between persons and organisations are extracted automatically from source text using a large language model pipeline guided by the [LACK ontology](ontology.html).

### Relation types extracted

| Source type | Relation | Target type |
|---|---|---|
| Person | contributed to | Organisation |
| Person or Organisation | is a member of | Organisation |
| Person | is employed by | Organisation |
| Person | is director of | Organisation |
| Person | is president of | Organisation |
| Organisation | same as | Organisation |
| Organisation | has partner | Organisation |
| Organisation | is associated with | Organisation |
| Organisation | sponsored | Person or Organisation |
| Organisation | was funded by | Person or Organisation |
| Organisation | is derived from | Organisation |
| Organisation | active since | Year |
| Organisation | active until | Year |

All relations can optionally carry **temporal annotations** (`since`, `until`, or `when`), represented via RDF reification.

### Evaluation

Evaluated on 300 relations extracted from 8 Desmog profile pages:

| Criterion | Yes | Partly | No | Accuracy | Accuracy (with partial) |
|---|---|---|---|---|---|
| True | 279 | 18 | 3 | 0.93 | 0.99 |
| Valid | 272 | 12 | 16 | 0.907 | 0.95 |
| Time info true | 239 | 34 | 27 | 0.797 | 0.91 |

Ongoing work includes error analysis, ontology refinement, and evaluation on LobbyMap sources.

---

## Entity Linking

Entities extracted from text are linked to canonical identifiers in Wikidata, enabling cross-source deduplication and enrichment.

Two methods have been implemented and compared:

- **Gemini in-context** — direct linking using a large language model
- **Multi-step workflow** — Wikidata search followed by LLM verification (using Groq + Llama 3.3 70B), including web search for disambiguation

The multi-step workflow shows better performance in preliminary evaluation. A gold standard is being prepared for formal evaluation. Entity linking over the full corpus is expected to complete shortly.

---

## Wikidata Enrichment

Linked entities can be enriched with information from Wikidata, including additional organisational roles, geographical context, and links to related claims and topics — supporting the research questions around alignment with climate science and policy goals.

---

## Roadmap

- [ ] Relation extraction error analysis and ontology refinement
- [ ] Entity linking gold standard evaluation
- [ ] Full-corpus entity linking completion
- [ ] Desmog claim clustering (pairwise similarity)
- [ ] Card categorisation
- [ ] Wikidata enrichment integration
- [ ] Knowledge graph publication and SPARQL endpoint
