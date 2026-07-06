#!/usr/bin/env bash
set -euo pipefail

# Clones the Daytona docs repo and regenerates skill references.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DOCS_REPO="https://github.com/daytona/docs.git"
DOCS_BRANCH="${1:-main}"
CLIENTS_REF="${DAYTONA_CLIENTS_REF:-main}"
TMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "Cloning daytona docs (branch: $DOCS_BRANCH)..."
git clone --depth 1 --branch "$DOCS_BRANCH" --filter=blob:none --sparse \
    "$DOCS_REPO" "$TMP_DIR/docs" 2>&1 | tail -1

cd "$TMP_DIR/docs"
git sparse-checkout set src/content/docs/en
cd "$REPO_ROOT"

DOCS_DIR="$TMP_DIR/docs/src/content/docs/en"
SPECS_DIR="$TMP_DIR/specs"
mkdir -p "$SPECS_DIR"

echo "Fetching OpenAPI specs from daytona/clients (ref: $CLIENTS_REF)..."
curl -fsSL "https://raw.githubusercontent.com/daytona/clients/${CLIENTS_REF}/openapi-specs/api.json" \
    -o "$SPECS_DIR/api.json"
curl -fsSL "https://raw.githubusercontent.com/daytona/clients/${CLIENTS_REF}/openapi-specs/toolbox.json" \
    -o "$SPECS_DIR/toolbox.json"

echo "Generating references..."
python3 "$SCRIPT_DIR/generate.py" "$DOCS_DIR" \
    --main-api-spec "$SPECS_DIR/api.json" \
    --toolbox-api-spec "$SPECS_DIR/toolbox.json"

echo "Done."
