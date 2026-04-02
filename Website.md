# LACK Website — Plan

## Overview

A static website for the **LACK (Lobbying Against Climate Knowledge)** knowledge graph project,
built from Markdown source files using a custom Python build script and deployed to GitHub Pages
via a GitHub Actions workflow.

---

## Repository Structure

```
lack/                                  ← repo root
├── content/                           ← all editable Markdown source files
│   ├── index.md                       ← Home page
│   ├── about.md                       ← Project background & motivation
│   ├── knowledge-graph.md             ← KG description (sources, extraction, linking)
│   ├── ontology.md                    ← Full ontology reference
│   └── download.md                    ← Download links for .ttl / .omn files
├── static/
│   ├── LACK.png                       ← Logo (copied from root)
│   └── style.css                      ← Site stylesheet
├── templates/
│   └── base.html                      ← Single HTML shell (nav, header, footer, {{ content }})
├── build.py                           ← Custom build script
├── config.yaml                        ← Site metadata (title, nav order, base_url)
├── lack-ontology.ttl                  ← Served verbatim
├── lack-ontology.omn                  ← Served verbatim
├── .github/
│   └── workflows/
│       └── deploy.yml                 ← GitHub Actions: build + publish to gh-pages
└── Website.md                         ← This file
```

Output of `build.py` goes to `_site/` (git-ignored). GitHub Pages is served from the `gh-pages`
branch, populated automatically by the action.

---

## Pages and Content

### `content/index.md` — Home
- Logo + one-liner: "A knowledge graph of actors and relationships involved in lobbying against
  climate science."
- Short paragraph on the project scope.
- Three call-to-action links: **About**, **Knowledge Graph**, **Ontology**, **Download**.
- Stats badge row (approximate, manually maintained): ~70k relations, 2 source corpora, 1 ontology.

### `content/about.md` — About
Derived from the slides. Covers:
- **Motivation**: questions the KG is designed to help answer, grouped into three themes —
  *Transparency & Disclosure* (who is lobbying, how are they funded, who are they meeting),
  *Alignment with Science & Policy* (are positions consistent with climate goals, what policies
  are they advocating), *Influence & Impact* (lobbying strategy, trusted messengers, conflicts
  of interest).
- **Sources**: Desmog (943 profile pages), LobbyMap/InfluenceMap (964 + 338 entries), with notes
  on additional candidate sources (SourceWatch, ClimatePolicyDatabase, Hot Air, Climate Files,
  Eco-Bot.Net, Climate Litigation Database).
- **Status**: active research project; links to ISWC 2026 target venue.
- **Team**: placeholder — to be filled in.

### `content/knowledge-graph.md` — Knowledge Graph
- **Relation extraction**: description of the IE pipeline, the relation types extracted (employed
  by, member of, funded by, founded, contributed to, etc.), accuracy figures (True: 0.93,
  Valid: 0.907, Time info: 0.797), and ~70k relations extracted.
- **Entity linking**: two methods (Gemini in-context; multi-step Wikidata search + LLM), moved to
  Groq Llama 3.3 70B for cost/speed; preliminary evaluation positive.
- **Wikidata enrichment**: importing additional context for entities (roles, topics, claims).
- **Current status & roadmap**: error analysis, ontology refinement, entity linking evaluation,
  Desmog claim clustering, card categorisation.

### `content/ontology.md` — Ontology
- Full content of `lack-ontology.md` (prefix, namespace, status, types, all relation sections,
  reification pattern, full vocabulary summary table).
- Note on schema.org alignment exercise (heavy reliance on `schema:memberOf + roleName`; inverse
  direction mismatches; no-match cases for domain-specific relations).
- Links to download the formal files.

### `content/download.md` — Download
- Table with two rows: `lack-ontology.ttl` and `lack-ontology.omn`, with format label, brief
  description, and download link.
- SPARQL endpoint / data dump placeholder for when the KG is published.
- Namespace and prefix reference block.

---

## `config.yaml`

```yaml
site_title: "LACK Knowledge Graph"
base_url: ""          # set to /repo-name if not served from root, e.g. /lack
nav:
  - label: "Home"
    file: "index.md"
  - label: "About"
    file: "about.md"
  - label: "Knowledge Graph"
    file: "knowledge-graph.md"
  - label: "Ontology"
    file: "ontology.md"
  - label: "Download"
    file: "download.md"
```

`base_url` is the only value that needs changing when the GitHub Pages URL is known.

---

## `build.py` — Custom Build Script

**Dependencies** (pip-installable, no build system): `markdown`, `pyyaml`

**Steps:**

1. Load `config.yaml`.
2. Clean and recreate `_site/`.
3. Copy `static/` → `_site/static/`.
4. Copy `lack-ontology.ttl` and `lack-ontology.omn` → `_site/`.
5. For each page in `nav`:
   a. Read the `.md` file from `content/`.
   b. Convert to HTML using the `markdown` library (with `tables` and `fenced_code` extensions).
   c. Load `templates/base.html`.
   d. Replace placeholders: `{{ site_title }}`, `{{ base_url }}`, `{{ nav }}`, `{{ page_title }}`,
      `{{ content }}`.
   e. Write to `_site/<slug>.html` (derived from the filename, `index.md` → `index.html`).
6. Print a summary of files written.

The nav is rendered as `<a class="active">` on the current page.

---

## `templates/base.html`

Single HTML file. Key regions:

- **`<head>`**: charset, viewport, `<title>{{ page_title }} — {{ site_title }}</title>`,
  link to `{{ base_url }}/static/style.css`.
- **`<header>`**: LACK.png logo + site title, linking to `index.html`.
- **`<nav>`**: `{{ nav }}` — injected by `build.py` as `<ul>` of links.
- **`<main>`**: `{{ content }}` — the converted Markdown HTML.
- **`<footer>`**: "LACK Knowledge Graph · Knowledge Media Institute · CC BY 4.0" (placeholder).

---

## `static/style.css`

Colour palette drawn from `LACK.png`:

| Role             | Colour      | Usage                                  |
|------------------|-------------|----------------------------------------|
| Background       | `#f0ede3`   | Warm off-white (matches logo bg)       |
| Primary dark     | `#2b2b2b`   | Text, borders, header bg               |
| Accent yellow    | `#d4b84a`   | Logo badge colour; nav hover, links    |
| Accent blue-grey | `#5a7fa3`   | Secondary accent (logo suit)           |
| White            | `#ffffff`   | Card/main content area                 |

Layout: single-column, max-width ~860px, centred. No JavaScript. Tables styled for the ontology
page (striped rows, horizontal scroll on small screens).

---

## `.github/workflows/deploy.yml`

Trigger: `push` to `main`.

Steps:
1. `actions/checkout@v4`
2. `actions/setup-python@v5` (Python 3.12)
3. `pip install markdown pyyaml`
4. `python build.py`
5. `actions/upload-pages-artifact@v3` (path: `_site`)
6. `actions/deploy-pages@v4`

Permissions: `pages: write`, `id-token: write`. GitHub Pages source must be set to
**GitHub Actions** in the repository settings (Settings → Pages → Source).

---

## Outstanding Decisions (needed before code generation)

1. **GitHub repo name / Pages URL** — needed to set `base_url` in `config.yaml`.
   e.g. `https://username.github.io/lack` → `base_url: /lack`
   or custom domain → `base_url: ""`

2. **Team / attribution** — who should appear in the footer or an About section?

3. **SPARQL endpoint** — is there a live one to link to on the Download page, or is that future work?

Everything else can be generated immediately once point 1 is confirmed.
