#!/usr/bin/env python3
"""
release.py — update the release metadata of the LACK website.

Called by deploy.sh after the lack-kgc files have been installed.
All figures come from lack-kgc; nothing is recomputed here. Reads:
  <kgc>/ontology/lack-kg.ttl   KG version, dates and licence
  KGSTATS.md                    all counts (copied from lack-kgc)
Writes:
  config.yaml                   release: block (used by build.py placeholders)
  lack-dataset.ttl              rendered from templates/lack-dataset.ttl.tmpl

Usage:
  python release.py --version 1.1 --kgc /path/to/lack-kgc --ref v1.1 --sha da81bb5
"""

import argparse
import os
import re
import sys

import yaml
from rdflib import Graph, URIRef, Namespace

from build import ROOT, CONFIG_FILE, KGSTATS_FILE, KGC_REPO_URL, parse_kgstats

DATASET_TMPL = os.path.join(ROOT, "templates", "lack-dataset.ttl.tmpl")
DATASET_FILE = os.path.join(ROOT, "lack-dataset.ttl")

KG   = URIRef("https://purl.net/climatesense/lack/dataset/kg")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
DC   = Namespace("http://purl.org/dc/terms/")
CC   = Namespace("http://creativecommons.org/ns#")


def die(msg):
    sys.exit(f"release.py: ERROR: {msg}")


def kg_metadata(kgc_dir):
    """Version, dates and licence of the KG, from lack-kgc/ontology/lack-kg.ttl."""
    path = os.path.join(kgc_dir, "ontology", "lack-kg.ttl")
    if not os.path.exists(path):
        die(f"{path} not found")
    g = Graph().parse(path, format="turtle")
    meta = {}
    for key, prop in [("version", DCAT.version), ("issued", DC.issued),
                      ("modified", DC.modified), ("license", CC.license)]:
        values = list(g.objects(KG, prop))
        if len(values) != 1:
            die(f"expected one {prop} for <{KG}> in {path}, found {len(values)}")
        meta[key] = str(values[0])
    return meta


def stat(stats, key):
    """Integer value of a KGSTATS.md placeholder; abort if missing."""
    value = stats.get(key)
    if value in (None, "", "0"):
        die(f"{key} missing from KGSTATS.md — is lack-kgc stats.sh up to date?")
    return int(str(value).replace(",", ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", required=True, help="expected KG version, e.g. 1.1")
    ap.add_argument("--kgc", required=True, help="path to a lack-kgc checkout at the release tag")
    ap.add_argument("--ref", required=True, help="lack-kgc tag or branch, e.g. v1.1")
    ap.add_argument("--sha", required=True, help="lack-kgc commit SHA")
    args = ap.parse_args()

    meta = kg_metadata(args.kgc)
    if meta["version"] != args.version:
        die(f"lack-kg.ttl declares version {meta['version']}, but {args.version} was requested")
    print(f"  KG v{meta['version']} — issued {meta['issued']}, modified {meta['modified']}, licence {meta['license']}")

    stats = parse_kgstats(KGSTATS_FILE)
    if not stats:
        die(f"{KGSTATS_FILE} missing or unreadable")

    # ── config.yaml ───────────────────────────────────────────────────────────
    with open(CONFIG_FILE, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    config["release"] = {
        "kg_version":  meta["version"],
        "kg_issued":   meta["issued"],
        "kg_modified": meta["modified"],
        "kg_license":  meta["license"],
        "kgc_ref":     args.ref,
        "kgc_sha":     args.sha,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, sort_keys=False, allow_unicode=True)
    print("  Updated config.yaml (release:)")

    # ── lack-dataset.ttl ──────────────────────────────────────────────────────
    values = {
        "kg_version":        meta["version"],
        "kg_issued":         meta["issued"],
        "kg_modified":       meta["modified"],
        "kg_license":        meta["license"],
        "kgc_url":           f"{KGC_REPO_URL}/tree/{args.ref}",
        "triples":           stat(stats, "kg_triples"),
        "distinct_subjects": stat(stats, "kg_distinct_subjects"),
        "entities":          stat(stats, "kg_total_entities"),
        "persons":           stat(stats, "kg_total_persons"),
        "collectives":       stat(stats, "kg_total_collectives"),
        "wikidata_links":    stat(stats, "kg_wikidata_links"),
        "dbpedia_links":     stat(stats, "kg_dbpedia_links"),
    }
    with open(DATASET_TMPL, encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: str(values.get(m.group(1), m.group(0))), text)
    left = re.findall(r"\{\{\s*\w+\s*\}\}", text)
    if left:
        die(f"unresolved placeholders in {DATASET_TMPL}: {sorted(set(left))}")
    with open(DATASET_FILE, "w", encoding="utf-8") as f:
        f.write(text)
    Graph().parse(DATASET_FILE, format="turtle")  # fails loudly if the rendered Turtle is invalid
    print(f"  Wrote lack-dataset.ttl ({values['triples']:,} triples, {values['entities']:,} entities)")


if __name__ == "__main__":
    main()