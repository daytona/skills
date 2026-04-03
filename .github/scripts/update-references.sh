#!/usr/bin/env bash
set -euo pipefail

# Clones the Daytona repo (sparse, docs only) and regenerates skill references.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DAYTONA_REPO="https://github.com/daytonaio/daytona.git"
DAYTONA_BRANCH="${1:-main}"
TMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "Cloning daytona docs (branch: $DAYTONA_BRANCH)..."
git clone --depth 1 --branch "$DAYTONA_BRANCH" --filter=blob:none --sparse \
    "$DAYTONA_REPO" "$TMP_DIR/daytona" 2>&1 | tail -1

cd "$TMP_DIR/daytona"
git sparse-checkout set apps/docs/src/content/docs/en libs/api-client-go/api libs/toolbox-api-client-go/api
cd "$REPO_ROOT"

DOCS_DIR="$TMP_DIR/daytona/apps/docs/src/content/docs/en"

echo "Generating references..."
python3 "$SCRIPT_DIR/generate.py" "$DOCS_DIR"

echo "Done."
