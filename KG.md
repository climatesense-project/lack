# LACK Knowledge Graph

LACK is a knowledge graph of entities (persons and organisations) and their relationships in the context of climate change lobbying and disinformation. It is constructed from two relation-extraction datasets — [Desmog](https://www.desmog.com) and [LobbyMap](https://lobbymap.org) — and grounded against Wikidata.

The graph uses the [LACK ontology](ontology/lack-ontology.ttl) (Lobbying and Climate Knowledge), which provides a small vocabulary of entity types and relationship properties designed for this domain.

## Files

| File | Description |
|---|---|
| `output/entities.ttl` | Named entities with types, labels, and Wikidata links |
| `output/relations.ttl` | Relations between entities with provenance and temporal data |

## Data model

### Entities (`output/entities.ttl`)

Each entity is a named individual of type `lack:Person` or `lack:Collective`, further classified by a granular subtype (e.g. `lack-type:company`, `lack-type:think_tank`, `lack-type:person`). Entity IRIs are stable SHA1 hashes of the best available external identifier, resolved in this order:

1. Wikidata QID
2. Wikipedia page URL
3. Web page URL
4. Surface form + evidence link (fallback)

### Relations (`output/relations.ttl`)

Each relation is represented as:
- A direct triple: `?source ?property ?target` using LACK ontology properties
- A reified `rdf:Statement` carrying provenance (`rdfs:seeAlso`) and optional temporal bounds (`lack:since`, `lack:until` as `xsd:gYear`)

## Statistics

### Entities

| | Count |
|---|---|
| **Total entities** | 13,120 |
| Persons (`lack:Person`) | 5,499 |
| Collectives (`lack:Collective`) | 7,648 |

Top collective subtypes:

| Subtype | Count |
|---|---|
| company | 2,107 |
| government_agency | 1,303 |
| foundation | 1,223 |
| think_tank | 1,057 |
| university | 386 |
| publication | 343 |
| consulting_firm | 192 |
| political_party | 162 |
| coalition | 158 |
| trade_association | 128 |
| program | 96 |
| industry_association | 91 |
| journal | 85 |
| political_campaign | 82 |
| pac | 72 |
| country | 56 |
| event | 50 |

### Relations

| | Count |
|---|---|
| **Total relation triples** | 65,527 |
| **Reified relation instances** | 77,168 |
| Instances with temporal data | 19,334 |
| Unique evidence sources | 2,180 |

The number of reified instances exceeds the number of distinct triples because the same logical relation can be attested by multiple evidence sources.

Relation distribution:

| Property | Triples |
|---|---|
| `lack:memberOf` | 16,434 |
| `lack:employedBy` | 9,559 |
| `lack:leadsAt` | 8,805 |
| `lack:contributedTo` | 8,550 |
| `lack:fundedBy` | 6,785 |
| `lack:hasPartner` | 4,693 |
| `lack:associatedWith` | 4,480 |
| `lack:sponsored` | 4,185 |
| `lack:derivedFrom` | 1,870 |
| `lack:founded` | 74 |
| `lack:hasMember` | 41 |
| `lack:acquired` | 38 |
| `lack:organised` | 13 |
| **Total** | **65,527** |
