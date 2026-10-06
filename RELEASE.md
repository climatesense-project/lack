# Release procedure (website)

The KG is built in [lack-kgc](https://github.com/enridaga/lack-kgc); see its
`RELEASE.md`. This repository publishes a tagged KG release on the website.

## What is versioned where

| Item | Source of truth | Copied to this repo by |
|---|---|---|
| KG version, dates and licence | `lack-kgc/ontology/lack-kg.ttl` | `release.py` → `config.yaml` (`release:`), `lack-dataset.ttl` |
| KG files | `lack-kgc/output/KG.tar.gz` | `deploy.sh` → `KG.ttl`, `KG-inferred.ttl`, `KG.zip` |
| KG statistics (all figures) | `lack-kgc/KGSTATS.md` | `deploy.sh` → `KGSTATS.md` |
| Ontology | `lack-kgc/ontology/lack-ontology.ttl` | `deploy.sh` → `lack-ontology.ttl` |
| Dataset description | `templates/lack-dataset.ttl.tmpl` | `release.py` → `lack-dataset.ttl` (generated, do not edit) |

No figures are computed in this repository: all counts come from `KGSTATS.md`.
The licence of the KG and of the ontology is CC BY-NC 4.0.

Website pages never contain hard-coded versions, dates or counts. They use
placeholders filled in by `build.py`:
- `{{ release_* }}` from `config.yaml` (`release:`)
- `{{ ontology_* }}` from `lack-ontology.ttl`
- `{{ kg_* }}` from `KGSTATS.md`

## Prerequisites

- The release is tagged `vX.Y` in lack-kgc.
- `git lfs`, `zip`, and `pip install pyyaml markdown rdflib`.

## 1. Deploy to a dev branch

    git checkout -b vX.Y-dev        # or an existing dev branch; never main
    ./deploy.sh X.Y                 # --no-push to keep everything local

`deploy.sh`: fetches lack-kgc at `vX.Y` → installs KG files and ontology →
updates release metadata → test-builds the site → commits and tags `vX.Y`
on the current branch → pushes branch and tag.

If the ontology changed, regenerate `lack-ontology.omn` by hand
(e.g. `robot convert -i lack-ontology.ttl -o lack-ontology.omn`) and commit it.

## 2. Review

    python build.py --local && (cd _site && python -m http.server)

Check the Home, Download, About and Ontology pages, and `lack-dataset.ttl`
(version, dates, licence, `void:triples` matching `KGSTATS.md`).
If something needs fixing, commit on the dev branch and move the tag:

    git tag -f -a vX.Y -m "LACK KG vX.Y" && git push -f origin vX.Y

## 3. Publish (manual)

    git checkout main
    git merge --no-ff vX.Y-dev -m "Release KG vX.Y"
    git push origin main

Pushing `main` triggers `.github/workflows/deploy.yml` (GitHub Pages).
Then:
- check the Actions run and the live site (version on Home, `KG.zip` downloads);
- create a GitHub release from tag `vX.Y`, using the lack-kgc `CHANGELOG.md` entry
  as release notes.