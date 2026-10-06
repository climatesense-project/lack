#!/usr/bin/env bash
#
# deploy.sh — install a LACK KG release from lack-kgc into this repository.
#
# Usage:  ./deploy.sh <version> [--no-push]      e.g.  ./deploy.sh 1.1
#
# Fetches lack-kgc at tag v<version>, installs the KG files and the ontology,
# updates all release metadata (config.yaml, lack-dataset.ttl), test-builds
# the site, then commits and tags v<version> on the CURRENT branch and pushes
# it. Publishing (merge into main) is manual: see RELEASE.md.
#
set -euo pipefail

KGC_REPO="${KGC_REPO:-https://github.com/enridaga/lack-kgc}"

die()  { echo "deploy.sh: ERROR: $*" >&2; exit 1; }
step() { echo; echo "==> $*"; }

[[ $# -ge 1 ]] || die "usage: ./deploy.sh <version> [--no-push]"
VERSION="$1"; TAG="v$VERSION"
PUSH=1; [[ "${2:-}" == "--no-push" ]] && PUSH=0
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+$ ]] || die "version must be MAJOR.MINOR (got '$VERSION')"

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# ── 1. Preflight ──────────────────────────────────────────────────────────────
step "Preflight"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ "$BRANCH" != "HEAD" ]] || die "detached HEAD; check out a branch first"
[[ "$BRANCH" != "main" ]] || die "on main; run on a dev branch (e.g. v${VERSION}-dev) and merge manually"
git diff --quiet && git diff --cached --quiet || die "working tree has uncommitted changes"
git lfs version >/dev/null 2>&1 || die "git lfs not installed"
command -v zip >/dev/null || die "zip not installed"
python3 -c "import yaml, markdown, rdflib" 2>/dev/null \
  || die "missing Python packages: pip install pyyaml markdown rdflib"
git rev-parse -q --verify "refs/tags/$TAG" >/dev/null && die "tag $TAG already exists locally"
if [[ $PUSH -eq 1 ]] && git ls-remote --exit-code --tags origin "$TAG" >/dev/null 2>&1; then
  die "tag $TAG already exists on origin"
fi
echo "Branch: $BRANCH   Release: $TAG   Push: $([[ $PUSH -eq 1 ]] && echo yes || echo no)"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# ── 2. Fetch lack-kgc ─────────────────────────────────────────────────────────
step "Fetching $KGC_REPO @ $TAG"
git -c advice.detachedHead=false clone -q --depth 1 --branch "$TAG" "$KGC_REPO" "$TMP/kgc" \
  || die "cannot clone $KGC_REPO at $TAG"
SHA="$(git -C "$TMP/kgc" rev-parse --short HEAD)"
echo "lack-kgc commit: $SHA"

# ── 3. Install files ──────────────────────────────────────────────────────────
step "Installing KG files and ontology"
tar -xzf "$TMP/kgc/output/KG.tar.gz" -C "$TMP" --exclude='._*'
[[ -s "$TMP/output/KG.ttl" && -s "$TMP/output/KG-inferred.ttl" ]] || die "KG.tar.gz lacks KG.ttl / KG-inferred.ttl"
cp "$TMP/output/KG.ttl"          KG.ttl
cp "$TMP/output/KG-inferred.ttl" KG-inferred.ttl
rm -f KG.zip
(cd "$TMP/output" && zip -q -X -9 "$ROOT/KG.zip" KG.ttl)
cp "$TMP/kgc/KGSTATS.md"                 KGSTATS.md
cp "$TMP/kgc/ontology/lack-ontology.ttl" lack-ontology.ttl
ls -l KG.ttl KG-inferred.ttl KG.zip KGSTATS.md lack-ontology.ttl

# ── 4–5. Release metadata ─────────────────────────────────────────────────────
step "Updating release metadata"
python3 release.py --version "$VERSION" --kgc "$TMP/kgc" --ref "$TAG" --sha "$SHA"

# ── 6. Test build ─────────────────────────────────────────────────────────────
step "Test build (python build.py --local)"
python3 build.py --local > "$TMP/build.log" 2>&1 || { cat "$TMP/build.log"; die "build failed"; }
grep -E "WARNING" "$TMP/build.log" || true
UNRESOLVED="$(grep -rhoE '\{\{ *(kg|release|ontology)_[a-zA-Z0-9_]+ *\}\}' _site --include='*.html' | sort -u || true)"
[[ -z "$UNRESOLVED" ]] || die "unresolved placeholders in _site: $UNRESOLVED"
if [[ -n "$(git diff --name-only -- lack-ontology.ttl)" ]]; then
  echo "NOTE: lack-ontology.ttl changed — regenerate lack-ontology.omn by hand (see RELEASE.md)."
fi

# ── 7. Commit, tag, push ──────────────────────────────────────────────────────
step "Commit and tag $TAG"
git add KG.ttl KG-inferred.ttl KG.zip KGSTATS.md lack-ontology.ttl lack-dataset.ttl config.yaml
git commit -q -m "KG $TAG (lack-kgc@$SHA)"
git tag -a "$TAG" -m "LACK KG $TAG (lack-kgc@$SHA)"
git --no-pager show --stat --oneline HEAD | head -20

if [[ $PUSH -eq 1 ]]; then
  step "Pushing $BRANCH and $TAG to origin"
  git push origin "$BRANCH"
  git push origin "$TAG"
fi

echo
echo "Done: $TAG committed on $BRANCH."
echo "To publish: review, merge $BRANCH into main and push main (see RELEASE.md)."