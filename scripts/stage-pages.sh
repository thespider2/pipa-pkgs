#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/repo.env"
REPO_DIR="$ROOT_DIR/repo/repo"
SITE_DIR="$ROOT_DIR/site"

source "$CONFIG_FILE"

rm -rf "$SITE_DIR"
mkdir -p "$SITE_DIR/repo"
cp -r "$REPO_DIR"/. "$SITE_DIR/repo/"

cat > "$SITE_DIR/index.html" <<EOF
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$REPO_NAME</title>
</head>
<body>
  <h1>$REPO_NAME</h1>
  <p>Pacman repository for Xiaomi Pad 6 / Pipa packages.</p>
  <p>Repo URL: <a href="$PAGES_BASE_URL/repo/">$PAGES_BASE_URL/repo/</a></p>
</body>
</html>
EOF

python "$ROOT_DIR/scripts/write_repo_index.py" "$SITE_DIR/repo"
