#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/repo.env"
REPO_DIR="$ROOT_DIR/repo/repo"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Missing config file: $CONFIG_FILE" >&2
    exit 1
fi

source "$CONFIG_FILE"

mkdir -p "$REPO_DIR"
rm -f "$REPO_DIR/$REPO_NAME.db"* "$REPO_DIR/$REPO_NAME.files"*

shopt -s nullglob
packages=("$REPO_DIR"/*.pkg.tar.zst "$REPO_DIR"/*.pkg.tar.xz)
shopt -u nullglob

if [ ${#packages[@]} -eq 0 ]; then
    echo "No package archives found under $REPO_DIR" >&2
    exit 1
fi

repo-add "$REPO_DIR/$REPO_NAME.db.tar.gz" "${packages[@]}"
