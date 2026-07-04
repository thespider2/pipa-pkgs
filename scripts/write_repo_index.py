#!/usr/bin/env python3
from pathlib import Path
import html
import sys


def write_index(directory: Path) -> None:
    dirs = sorted(p.name for p in directory.iterdir() if p.is_dir() and not p.name.startswith('.'))
    files = sorted(p.name for p in directory.iterdir() if p.is_file() and p.name != 'index.html')
    lines = [
        '<!doctype html>',
        '<html lang="en">',
        f'<head><meta charset="utf-8"><title>Index of /{directory.name}/</title></head>',
        '<body>',
        f'<h1>Index of /{directory.name}/</h1>',
        '<ul>',
    ]
    for d in dirs:
        safe = html.escape(d)
        lines.append(f'<li><a href="{safe}/">{safe}/</a></li>')
    for f in files:
        safe = html.escape(f)
        lines.append(f'<li><a href="{safe}">{safe}</a></li>')
    lines.extend(['</ul>', '</body>', '</html>'])
    (directory / 'index.html').write_text('\n'.join(lines) + '\n')

    for child in directory.iterdir():
        if child.is_dir() and not child.name.startswith('.'):
            write_index(child)


write_index(Path(sys.argv[1]))
