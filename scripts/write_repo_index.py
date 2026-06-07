#!/usr/bin/env python3
from pathlib import Path
import html
import sys

repo_dir = Path(sys.argv[1])
entries = sorted(p.name for p in repo_dir.iterdir() if p.is_file())
lines = [
    '<!doctype html>',
    '<html lang="en">',
    '<head><meta charset="utf-8"><title>Repo Index</title></head>',
    '<body>',
    '<h1>Repo Index</h1>',
    '<ul>',
]
for entry in entries:
    safe = html.escape(entry)
    lines.append(f'<li><a href="{safe}">{safe}</a></li>')
lines.extend(['</ul>', '</body>', '</html>'])
(repo_dir / 'index.html').write_text('\n'.join(lines) + '\n')
