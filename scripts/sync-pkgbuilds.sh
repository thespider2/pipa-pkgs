#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/repo.env"
TARGET_DIR="$ROOT_DIR"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Missing config file: $CONFIG_FILE" >&2
    exit 1
fi

source "$CONFIG_FILE"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

git clone --depth 1 --branch "${SOURCE_SYNC_REPO_REF:-main}" "${SOURCE_SYNC_REPO_URL:?}" "$WORK_DIR/source"
rsync -a --delete "$WORK_DIR/source/pipa-endeavouros-builder/common/" "$TARGET_DIR/common/"
rsync -a --delete "$WORK_DIR/source/pipa-endeavouros-builder/sm8250/" "$TARGET_DIR/sm8250/"

echo "Synced pkgs into $TARGET_DIR/{common,sm8250}"
