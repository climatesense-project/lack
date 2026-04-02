---
title: Ontology
---

# LACK Ontology

**Prefix:** `lack:`  
**Namespace:** `http://lack.climatesense.kmi.tools#`  
**Status:** Draft

Download the formal files: [Turtle (.ttl)](lack-ontology.ttl) · [Manchester Syntax (.omn)](lack-ontology.omn)

---

## Overview

LACK is a lightweight ontology for describing relationships between people and organisations, derived from a large corpus of real-world relation expressions relevant to lobbying against climate change awareness and policies. It provides a minimal, reusable vocabulary covering membership, employment, leadership, funding, founding, and association.

The ontology is built around two top-level types and a set of object properties connecting them.

---

## Types

### `lack:Person`
An individual human being.

### `lack:Collective`
Any group of people organised around a shared purpose. This includes but is not limited to: companies, NGOs, think tanks, news agencies, political assemblies, events, committees, and networks.

---

## Relations

### Membership

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:memberOf` | member of | `lack:Person` | `lack:Collective` | `lack:hasMember` | `lack:associatedWith` |
| `lack:hasMember` | has member | `lack:Collective` | `lack:Person` | `lack:memberOf` | `lack:associatedWith` |

### Employment

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:employedBy` | employed by | `lack:Person` | `lack:Collective` | `lack:hasEmployee` | `lack:associatedWith` |
| `lack:hasEmployee` | has employee | `lack:Collective` | `lack:Person` | `lack:employedBy` | `lack:associatedWith` |

### Leadership

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:leadsAt` | leads at | `lack:Person` | `lack:Collective` | `lack:hasLeader` | `lack:employedBy` |
| `lack:hasLeader` | has leader | `lack:Collective` | `lack:Person` | `lack:leadsAt` | `lack:associatedWith` |

`lack:leadsAt` covers any named leadership or responsibility role within an organisation or department, including but not limited to: CEO, president, chair, director, VP, treasurer, secretary, COO, and department-level director roles. It is a sub-property of `lack:employedBy`, which is itself a sub-property of `lack:associatedWith`.

### Funding

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:fundedBy` | funded by | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:hasFunder` | `lack:associatedWith` |
| `lack:hasFunder` | has funder | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:fundedBy` | `lack:associatedWith` |

Covers funding, donation, commissioning, and award receipt.

### Founding & Creation

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:founded` | founded | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasFoundedBy` | `lack:associatedWith` |
| `lack:wasFoundedBy` | was founded by | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:founded` | `lack:associatedWith` |

Covers founding, co-founding, creation, incorporation, and launch.

### Contribution

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:contributedTo` | contributed to | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:hasContributor` | |
| `lack:hasContributor` | has contributor | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:contributedTo` | |

Covers contribution, authorship, distribution, presentation, and reposting.

### Partnership

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:hasPartner` | has partner | `lack:Collective` | `lack:Collective` | `lack:hasPartner` *(symmetric)* | `lack:associatedWith` |

### Sponsorship

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:sponsored` | sponsored | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:wasSponsoredBy` | `lack:associatedWith` |
| `lack:wasSponsoredBy` | was sponsored by | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:sponsored` | `lack:associatedWith` |

Covers sponsorship, promotion, patronage, and support.

### Association

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:associatedWith` | associated with | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:associatedWith` *(symmetric)* | |

General-purpose association or affiliation. Used when no more specific relation applies. This is the top-level relation from which most other relations in this ontology are derived.

### Ownership & Acquisition

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:acquired` | acquired | `lack:Collective` | `lack:Collective` | `lack:wasAcquiredBy` | `lack:associatedWith` |
| `lack:wasAcquiredBy` | was acquired by | `lack:Collective` | `lack:Collective` | `lack:acquired` | `lack:associatedWith` |

Covers acquisition, ownership, controlling interest, and shareholding.

### Derivation

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:derivedFrom` | derived from | `lack:Collective` | `lack:Collective` | `lack:hasDerivation` | `lack:associatedWith` |
| `lack:hasDerivation` | has derivation | `lack:Collective` | `lack:Collective` | `lack:derivedFrom` | `lack:associatedWith` |

### Event Organisation

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `lack:organised` | organised | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasOrganisedBy` | `lack:associatedWith` |
| `lack:wasOrganisedBy` | was organised by | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:organised` | `lack:associatedWith` |

### Identity & Naming

We reuse `owl:sameAs` to cover identity, renaming, aliases, and doing-business-as relations.

| Term | Label | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|---|
| `owl:sameAs` | same as | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `owl:sameAs` *(symmetric)* | |

### Temporal Activity (entity-level)

These datatype properties attach temporal bounds directly to a `lack:Person` or `lack:Collective`.

| Term | Label | Domain | Range | Note |
|---|---|---|---|---|
| `lack:activeSince` | active since | `lack:Person` \| `lack:Collective` | `xsd:gYear` | Datatype property — no inverse |
| `lack:activeUntil` | active until | `lack:Person` \| `lack:Collective` | `xsd:gYear` | Datatype property — no inverse |

---

## Reification of Temporal Relations

When a relation is annotated with temporal information (`since`, `until`, or `when`), it is represented using **RDF reification** (`rdf:Statement`). The base triple is always asserted directly in addition to the reified statement.

| Term | Label | Domain | Range | Note |
|---|---|---|---|---|
| `lack:since` | since | `rdf:Statement` | `xsd:gYear` | Start year of the relation |
| `lack:until` | until | `rdf:Statement` | `xsd:gYear` | End year of the relation |

When the source annotation is `when` (a point in time rather than an interval), both `lack:since` and `lack:until` are set to the same year value.

### Example

```turtle
# Base triple always asserted
:Alice lack:employedBy :Org .

# Reified statement with interval
:stmt1 a rdf:Statement ;
    rdf:subject   :Alice ;
    rdf:predicate lack:employedBy ;
    rdf:object    :Org ;
    lack:since    "2010"^^xsd:gYear ;
    lack:until    "2020"^^xsd:gYear .

# Reified statement with point-in-time (when → since = until)
:stmt2 a rdf:Statement ;
    rdf:subject   :Alice ;
    rdf:predicate lack:memberOf ;
    rdf:object    :BoardX ;
    lack:since    "2015"^^xsd:gYear ;
    lack:until    "2015"^^xsd:gYear .
```

---

## Full Vocabulary Summary

| Term | Domain | Range | Inverse | Sub-property of |
|---|---|---|---|---|
| `lack:memberOf` | `lack:Person` | `lack:Collective` | `lack:hasMember` | `lack:associatedWith` |
| `lack:hasMember` | `lack:Collective` | `lack:Person` | `lack:memberOf` | `lack:associatedWith` |
| `lack:employedBy` | `lack:Person` | `lack:Collective` | `lack:hasEmployee` | `lack:associatedWith` |
| `lack:hasEmployee` | `lack:Collective` | `lack:Person` | `lack:employedBy` | `lack:associatedWith` |
| `lack:leadsAt` | `lack:Person` | `lack:Collective` | `lack:hasLeader` | `lack:employedBy` |
| `lack:hasLeader` | `lack:Collective` | `lack:Person` | `lack:leadsAt` | `lack:associatedWith` |
| `lack:fundedBy` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:hasFunder` | `lack:associatedWith` |
| `lack:hasFunder` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:fundedBy` | `lack:associatedWith` |
| `lack:founded` | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasFoundedBy` | `lack:associatedWith` |
| `lack:wasFoundedBy` | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:founded` | `lack:associatedWith` |
| `lack:contributedTo` | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:hasContributor` | |
| `lack:hasContributor` | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:contributedTo` | |
| `lack:hasPartner` | `lack:Collective` | `lack:Collective` | *(symmetric)* | `lack:associatedWith` |
| `lack:sponsored` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:wasSponsoredBy` | `lack:associatedWith` |
| `lack:wasSponsoredBy` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:sponsored` | `lack:associatedWith` |
| `lack:associatedWith` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | *(symmetric)* | |
| `lack:acquired` | `lack:Collective` | `lack:Collective` | `lack:wasAcquiredBy` | `lack:associatedWith` |
| `lack:wasAcquiredBy` | `lack:Collective` | `lack:Collective` | `lack:acquired` | `lack:associatedWith` |
| `lack:derivedFrom` | `lack:Collective` | `lack:Collective` | `lack:hasDerivation` | `lack:associatedWith` |
| `lack:hasDerivation` | `lack:Collective` | `lack:Collective` | `lack:derivedFrom` | `lack:associatedWith` |
| `lack:organised` | `lack:Person` \| `lack:Collective` | `lack:Collective` | `lack:wasOrganisedBy` | `lack:associatedWith` |
| `lack:wasOrganisedBy` | `lack:Collective` | `lack:Person` \| `lack:Collective` | `lack:organised` | `lack:associatedWith` |
| `owl:sameAs` | `lack:Person` \| `lack:Collective` | `lack:Person` \| `lack:Collective` | *(symmetric)* | |
| `lack:activeSince` | `lack:Person` \| `lack:Collective` | `xsd:gYear` | *(datatype property)* | |
| `lack:activeUntil` | `lack:Person` \| `lack:Collective` | `xsd:gYear` | *(datatype property)* | |
| `lack:since` | `rdf:Statement` | `xsd:gYear` | *(datatype property — reification)* | |
| `lack:until` | `rdf:Statement` | `xsd:gYear` | *(datatype property — reification)* | |

---

## Schema.org Alignment

A mapping exercise to schema.org has been conducted. Key findings:

- **Heavy reliance on `schema:memberOf + roleName`** — schema.org has no dedicated properties for most named organisational roles (CEO, chair, treasurer, VP, etc.). The recommended pattern is to use `schema:memberOf` with a `schema:Role` wrapper and a `roleName` literal to capture the specific title.
- **Inverse direction mismatches** — many relations (funded, published, created, employed) are naturally expressed person→org in LACK, but schema.org models the predicate on the receiving entity (e.g. `schema:funder` is a property of the funded thing).
- **No-match cases** — highly specific operational or contractual relations (lobbied for, conducted public relations for, created a crisis plan for, launched, incorporated) have no schema.org equivalent and are better represented with custom predicates in a domain-specific vocabulary such as LACK.
