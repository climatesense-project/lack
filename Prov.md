# LACK Provenance Notes

## Overview

Each relation instance in the LACK knowledge graph is represented as a reified `rdf:Statement` (see `lack-ontology.md`). Provenance metadata is attached to these statement instances using **PROV-O** (`prov:`) and **Dublin Core Terms** (`dct:`).

Two shared provenance resources are declared once in the dataset and referenced by all statement instances:

---

## Provenance resources

### `lack:lackAgent`

The AI agent that automatically extracted relations from web pages.

```turtle
lack:lackAgent a prov:Agent , prov:SoftwareAgent ;
    rdfs:label "LACK extraction agent"@en ;
    rdfs:comment "AI agent designed and developed by the Knowledge Media Institute (KMi) for automated relation extraction from web pages."@en ;
    dct:creator <https://kmi.open.ac.uk> .
```

### `lack:lackActivity`

The extraction activity carried out by `lack:lackAgent` between January and March 2026.

```turtle
lack:lackActivity a prov:Activity ;
    rdfs:label "LACK automated extraction"@en ;
    rdfs:comment "Automated extraction of relations from web pages, performed by the KMi AI agent between January and March 2026."@en ;
    prov:startedAtTime  "2026-01"^^xsd:gYearMonth ;
    prov:endedAtTime    "2026-03"^^xsd:gYearMonth ;
    prov:wasAssociatedWith lack:lackAgent .
```

---

## Attaching provenance to a reified statement

Every `rdf:Statement` instance should include:

- `dct:source` — the URL of the source web page the relation was extracted from
- `prov:wasGeneratedBy` — pointing to `lack:lackActivity`

```turtle
# Base triple always asserted
:Alice lack:employedBy :Org .

# Reified statement with temporal and provenance metadata
:stmt1 a rdf:Statement ;
    rdf:subject            :Alice ;
    rdf:predicate          lack:employedBy ;
    rdf:object             :Org ;
    lack:since             "2010"^^xsd:gYear ;
    lack:until             "2020"^^xsd:gYear ;
    dct:source             <https://example.org/source-page> ;
    prov:wasGeneratedBy    lack:lackActivity .
```

---

## Required prefixes

```turtle
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix dct:  <http://purl.org/dc/terms/> .
```

Both are well-supported in Virtuoso Open Source.

---

## Status

`lack:lackAgent` and `lack:lackActivity` are not yet added to the knowledge graph. They should be declared once as named individuals when the KG is populated.
