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

The LACK knowledge graph v{{ release_version }} (released {{ release_modified_long }}) is available for download under [CC BY-NC 4.0]({{ release_license }}). See the [changelog]({{ release_changelog_url }}) for what changed between versions.

| File | Format | Description |
|---|---|---|
| [KG.zip]({{ base_url }}/KG.zip) | Turtle (RDF), zipped | Knowledge graph v{{ release_version }} — asserted + inferred triples ({{ kg_triples }} triples) |
| [lack-dataset.ttl]({{ base_url }}/lack-dataset.ttl) | Turtle (RDF) | Dataset description (DCAT, VoID) |

Built from [lack-kgc {{ release_kgc_ref }}]({{ release_kgc_url }}).

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

The LACK ontology and data are released under [CC BY NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). Please cite the ClimateSense project when using this resource.
