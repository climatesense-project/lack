---
title: Knowledge Graph
---

# The LACK Knowledge Graph

The LACK knowledge graph is constructed through a three-phase pipeline of relation extraction from web pages, ontology alignment, entity URI generation, and relation graph construction, applied to relation extraction datasets from two investigative journalism sources covering climate lobbying.

---

## KG at a Glance

### Entities

| | Count |
|---|---|
| **Total entities** | **{{ kg_total_entities }}** |
| Persons (`lack:Person`) | {{ kg_total_persons }} |
| Collectives (`lack:Collective`) | {{ kg_total_collectives }} |
| Wikidata links (`owl:sameAs`) | {{ kg_wikidata_links }} |
| DBpedia links | {{ kg_dbpedia_links }} |

### Relations

| | Count |
|---|---|
| **Asserted (extracted)** | **{{ kg_asserted }}** |
| **Inferred (entailed)** | **{{ kg_inferred }}** |
| **Total after inferencing** | **{{ kg_total }}** |

---

## Relation Extraction

Relationships between persons and organisations are extracted automatically from source text using a large language model pipeline guided by the [LACK ontology](ontology.html).

### Relation types extracted

| Relation | Count |
|---|---|
| `lack:memberOf` | {{ kg_rel_memberOf }} |
| `lack:employedBy` | {{ kg_rel_employedBy }} |
| `lack:leadsAt` | {{ kg_rel_leadsAt }} |
| `lack:contributedTo` | {{ kg_rel_contributedTo }} |
| `lack:fundedBy` | {{ kg_rel_fundedBy }} |
| `lack:hasPartner` | {{ kg_rel_hasPartner }} |
| `lack:associatedWith` | {{ kg_rel_associatedWith }} |
| `lack:sponsored` | {{ kg_rel_sponsored }} |
| `lack:derivedFrom` | {{ kg_rel_derivedFrom }} |
| `lack:founded` | {{ kg_rel_founded }} |
| `lack:hasMember` | {{ kg_rel_hasMember }} |
| `lack:acquired` | {{ kg_rel_acquired }} |
| `lack:organised` | {{ kg_rel_organised }} |
| **Total** | **{{ kg_asserted }}** |

### Attributes

Temporal bounds attached directly to entities (rather than to relations):

| Attribute | Count |
|---|---|
| `lack:activeSince` | {{ kg_attr_activeSince }} |
| `lack:activeUntil` | {{ kg_attr_activeUntil }} |
| **Total** | **{{ kg_attr_total }}** |

### Reified Statements

All extracted relations are represented as reified `rdf:Statement` instances, enabling provenance metadata (source URL, temporal bounds) to be attached to individual relation assertions. The total number of statements ({{ kg_statements_total }}) exceeds the number of distinct relations because some entity pairs are attested by multiple sources.

| Relation | Statements |
|---|---|
| `lack:memberOf` | {{ kg_stmt_memberOf }} |
| `lack:contributedTo` | {{ kg_stmt_contributedTo }} |
| `lack:leadsAt` | {{ kg_stmt_leadsAt }} |
| `lack:employedBy` | {{ kg_stmt_employedBy }} |
| `lack:fundedBy` | {{ kg_stmt_fundedBy }} |
| `lack:associatedWith` | {{ kg_stmt_associatedWith }} |
| `lack:sponsored` | {{ kg_stmt_sponsored }} |
| `lack:hasPartner` | {{ kg_stmt_hasPartner }} |
| `lack:derivedFrom` | {{ kg_stmt_derivedFrom }} |
| `lack:activeSince` | {{ kg_stmt_activeSince }} |
| `owl:sameAs` | {{ kg_stmt_owl_sameAs }} |
| `lack:activeUntil` | {{ kg_stmt_activeUntil }} |
| `lack:founded` | {{ kg_stmt_founded }} |
| `lack:hasMember` | {{ kg_stmt_hasMember }} |
| `lack:acquired` | {{ kg_stmt_acquired }} |
| `lack:organised` | {{ kg_stmt_organised }} |
| **Total** | **{{ kg_statements_total }}** |

All relations can optionally carry **temporal annotations** (`since`, `until`), represented via RDF reification on the `rdf:Statement` node.

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

Entities extracted from text are linked to canonical identifiers in Wikidata and DBpedia, enabling cross-source deduplication and enrichment. Entity linking is complete for v1.0.

Two methods were implemented and compared:

- **Gemini in-context** — direct linking using a large language model
- **Multi-step workflow** — Wikidata search followed by LLM verification (Groq + Llama 3.3 70B), including web search for disambiguation

The multi-step workflow was selected for production. Coverage in the current release:

| | Count | % of entities |
|---|---|---|
| Wikidata links | {{ kg_wikidata_links }} | {{ kg_wikidata_pct }} |
| DBpedia links | {{ kg_dbpedia_links }} | {{ kg_dbpedia_pct }} |
| Unlinked entities | {{ kg_unlinked }} | {{ kg_unlinked_pct }} |

Entity links are represented using two distinct properties reflecting different certainty levels: `owl:sameAs` asserts identity between the LACK entity and the external URI, while `rdfs:seeAlso` indicates a related but not necessarily identical resource.

| Link type | Count |
|---|---|
| `owl:sameAs` | {{ kg_sameas_owl }} |
| `rdfs:seeAlso` | {{ kg_sameas_rdfs }} |
| **Total** | **{{ kg_sameas_total }}** |

---

## Inferencing

After the asserted graph is constructed, OWL inferencing is applied using the LACK ontology to materialise:

- **Inverse properties** — e.g. every `lack:employedBy` triple generates a `lack:hasEmployee` triple; every `lack:memberOf` generates `lack:hasMember`
- **`lack:associatedWith` entailments** — as the top-level superproperty, it is entailed by all other relation types

This adds {{ kg_inferred }} triples, bringing the total graph to **{{ kg_total }} triples**.

| | Count |
|---|---|
| Asserted triples | {{ kg_asserted_inf }} |
| Inferred triples | {{ kg_inferred_inf }} |
| **Total** | **{{ kg_total_inf }}** |

### Inferred relation breakdown

| Relation | Count |
|---|---|
| `lack:associatedWith` | {{ kg_inf_rel_associatedWith }} |
| `lack:hasMember` | {{ kg_inf_rel_hasMember }} |
| `lack:hasEmployee` | {{ kg_inf_rel_hasEmployee }} |
| `lack:hasContributor` | {{ kg_inf_rel_hasContributor }} |
| `lack:employedBy` | {{ kg_inf_rel_employedBy }} |
| `lack:hasLeader` | {{ kg_inf_rel_hasLeader }} |
| `lack:hasFunder` | {{ kg_inf_rel_hasFunder }} |
| `lack:wasSponsoredBy` | {{ kg_inf_rel_wasSponsoredBy }} |
| `lack:hasPartner` | {{ kg_inf_rel_hasPartner }} |
| `lack:hasDerivation` | {{ kg_inf_rel_hasDerivation }} |
| `lack:wasFoundedBy` | {{ kg_inf_rel_wasFoundedBy }} |
| `lack:memberOf` | {{ kg_inf_rel_memberOf }} |
| `lack:wasAcquiredBy` | {{ kg_inf_rel_wasAcquiredBy }} |
| `lack:wasOrganisedBy` | {{ kg_inf_rel_wasOrganisedBy }} |
| **Total** | **{{ kg_inferred }}** |

---

