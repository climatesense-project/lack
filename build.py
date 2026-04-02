#!/usr/bin/env python3
"""
build.py — LACK Knowledge Graph static site builder.

Usage:
    python build.py

Reads:  config.yaml, content/*.md, templates/base.html, static/, *.ttl, *.omn
Writes: _site/
"""

import os
import re
import shutil
import yaml
import markdown as md_lib

# ── Paths ──────────────────────────────────────────────────────────────────────

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "content")
STATIC_DIR = os.path.join(ROOT, "static")
TEMPLATE_FILE = os.path.join(ROOT, "templates", "base.html")
CONFIG_FILE = os.path.join(ROOT, "config.yaml")
OUTPUT_DIR = os.path.join(ROOT, "_site")

# Extra files to copy verbatim into _site root
VERBATIM_FILES = ["lack-ontology.ttl", "lack-ontology.omn"]

# ── Helpers ────────────────────────────────────────────────────────────────────

def load_config():
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_template():
    with open(TEMPLATE_FILE, encoding="utf-8") as f:
        return f.read()


def parse_frontmatter(text):
    """Strip YAML frontmatter (--- ... ---) and return (meta_dict, body)."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if match:
        meta = yaml.safe_load(match.group(1)) or {}
        body = text[match.end():]
    else:
        meta = {}
        body = text
    return meta, body


def slug_from_filename(filename):
    """'about.md' → 'about'"""
    return os.path.splitext(filename)[0]


def html_filename(md_filename):
    """'about.md' → 'about.html'"""
    return slug_from_filename(md_filename) + ".html"


def build_nav(nav_items, base_url, current_slug):
    """Render the <nav> <ul> items, marking the active page."""
    items = []
    for item in nav_items:
        slug = slug_from_filename(item["file"])
        href = f"{base_url}/{html_filename(item['file'])}"
        active = ' class="active"' if slug == current_slug else ""
        items.append(f'      <li><a href="{href}"{active}>{item["label"]}</a></li>')
    return "\n".join(items)


def render_page(template, content_html, page_title, nav_html, site_title, base_url):
    """Substitute all placeholders in the base template and content."""
    # Apply base_url substitution to content first (for links in markdown)
    content_html = content_html.replace("{{ base_url }}", base_url)
    out = template
    out = out.replace("{{ page_title }}", page_title)
    out = out.replace("{{ site_title }}", site_title)
    out = out.replace("{{ base_url }}", base_url)
    out = out.replace("{{ nav }}", nav_html)
    out = out.replace("{{ content }}", content_html)
    return out


# ── Build ──────────────────────────────────────────────────────────────────────

def main():
    config = load_config()
    site_title = config["site_title"]
    base_url = config.get("base_url", "").rstrip("/")
    nav_items = config["nav"]

    template = load_template()

    # Clean and recreate output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy static assets
    out_static = os.path.join(OUTPUT_DIR, "static")
    shutil.copytree(STATIC_DIR, out_static)
    print(f"  Copied static/ → _site/static/")

    # Copy verbatim files (ontology)
    for fname in VERBATIM_FILES:
        src = os.path.join(ROOT, fname)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(OUTPUT_DIR, fname))
            print(f"  Copied {fname} → _site/{fname}")
        else:
            print(f"  WARNING: {fname} not found, skipping.")

    # Markdown extensions
    md_extensions = ["tables", "fenced_code", "attr_list", "def_list"]

    # Build each page
    for item in nav_items:
        md_file = item["file"]
        md_path = os.path.join(CONTENT_DIR, md_file)

        if not os.path.exists(md_path):
            print(f"  WARNING: {md_path} not found, skipping.")
            continue

        with open(md_path, encoding="utf-8") as f:
            raw = f.read()

        meta, body = parse_frontmatter(raw)
        page_title = meta.get("title", item["label"])

        content_html = md_lib.markdown(body, extensions=md_extensions)

        current_slug = slug_from_filename(md_file)
        nav_html = build_nav(nav_items, base_url, current_slug)

        page_html = render_page(
            template, content_html, page_title, nav_html, site_title, base_url
        )

        out_filename = html_filename(md_file)
        out_path = os.path.join(OUTPUT_DIR, out_filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(f"  Built {md_file} → _site/{out_filename}")

    print(f"\nDone. Site written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
