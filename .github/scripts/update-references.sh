#!/usr/bin/env bash
set -euo pipefail

# Clones the Daytona docs and clients repos (sparse) and regenerates skill references.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DOCS_REPO="${DOCS_REPO:-https://github.com/daytona/docs.git}"
DOCS_BRANCH="${1:-main}"
CLIENTS_REPO="${CLIENTS_REPO:-https://github.com/daytona/clients.git}"
CLIENTS_BRANCH="${2:-main}"
TMP_DIR=$(mktemp -d)

cleanup() { rm -rf "$TMP_DIR"; }
trap cleanup EXIT

echo "Cloning daytona docs (branch: $DOCS_BRANCH)..."
git clone --depth 1 --branch "$DOCS_BRANCH" --filter=blob:none --sparse \
    "$DOCS_REPO" "$TMP_DIR/docs" 2>&1 | tail -1
git -C "$TMP_DIR/docs" sparse-checkout set src/content/docs/en

echo "Cloning daytona clients (branch: $CLIENTS_BRANCH)..."
git clone --depth 1 --branch "$CLIENTS_BRANCH" --filter=blob:none --sparse \
    "$CLIENTS_REPO" "$TMP_DIR/clients" 2>&1 | tail -1
git -C "$TMP_DIR/clients" sparse-checkout set api-client-go/api toolbox-api-client-go/api

echo "Generating references..."
python3 "$SCRIPT_DIR/generate.py" "$TMP_DIR/docs/src/content/docs/en" "$TMP_DIR/clients"

echo "Done."
