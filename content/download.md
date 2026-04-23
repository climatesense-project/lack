---
title: Download
---

# Download

## Ontology Files

The LACK ontology is available in two serialisations:

| File | Format | Description |
|---|---|---|
| [lack-ontology.ttl]({{ base_url }}/lack-ontology.ttl) | Turtle (RDF) | Primary serialisation |
| [lack-ontology.omn]({{ base_url }}/lack-ontology.omn) | Manchester Syntax (OWL) | For use with Protégé and OWL tools |

### Namespace and Prefix

```
Prefix:  lack:
URI:     https://purl.net/climatesense/lack/ns#
```

---

## Knowledge Graph Data

The LACK knowledge graph v1.0 (released 23 April 2026) is available for download.

| File | Format | Description |
|---|---|---|
| [KG.ttl]({{ base_url }}/KG.ttl) | Turtle (RDF) | Knowledge graph v1.0 — asserted + inferred triples |

Check the [GitHub repository](https://github.com/climatesense-project/lack) for updates.

---

## SPARQL Endpoint

The LACK knowledge graph is available as a live SPARQL endpoint powered by [QLever](https://github.com/ad-freiburg/qlever):

```
https://sparql.climatesense.kmi.tools/climatesense
```

You can query it interactively using the [Explore](explore/explore.html) page, or from any SPARQL client by sending queries with `Accept: application/sparql-results+json`.

---

## Licence

The LACK ontology and data are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the ClimateSense project when using this resource.
