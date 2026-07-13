#!/usr/bin/env python3
from __future__ import annotations

import io
import tarfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config'
OUTPUT_DIR = ROOT / 'repo' / 'repo'
ENV_PATH = CONFIG / 'repo.env'
PACKAGES_PATH = CONFIG / 'packages.upstream.txt'


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        env[key.strip()] = value.strip()
    return env


def parse_desc(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith('%') and line.endswith('%'):
            current = line
            result.setdefault(current, [])
        elif current is not None:
            result[current].append(line)
    return result


def main() -> int:
    env = load_env(ENV_PATH)
    upstream_url = env['UPSTREAM_REPO_URL'].rstrip('/') + '/'
    db_name = env['UPSTREAM_DB_NAME']
    wanted = {
        line.strip()
        for line in PACKAGES_PATH.read_text().splitlines()
        if line.strip() and not line.strip().startswith('#')
    }

    if not wanted:
        print('No upstream packages requested; skipping mirror step.')
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    db_url = f"{upstream_url}{db_name}.db.tar.gz"
    print(f"Fetching upstream database: {db_url}")
    try:
        with urllib.request.urlopen(db_url) as response:
            data = response.read()
    except urllib.error.HTTPError as exc:
        print(
            f"WARNING: upstream database unavailable ({exc.code} {exc.reason}); "
            f"skipping mirror of: {', '.join(sorted(wanted))}"
        )
        return 0
    except urllib.error.URLError as exc:
        print(
            f"WARNING: upstream database unreachable ({exc.reason}); "
            f"skipping mirror of: {', '.join(sorted(wanted))}"
        )
        return 0

    tf = tarfile.open(fileobj=io.BytesIO(data), mode='r:gz')
    found: dict[str, str] = {}
    for member in tf.getmembers():
        if not member.name.endswith('/desc'):
            continue
        extracted = tf.extractfile(member)
        if extracted is None:
            continue
        desc = parse_desc(extracted.read().decode('utf-8', 'replace'))
        name = desc.get('%NAME%', [''])[0]
        filename = desc.get('%FILENAME%', [''])[0]
        if name in wanted and filename:
            found[name] = filename

    missing = sorted(wanted - set(found))
    if missing:
        print(
            f"WARNING: missing packages in upstream database "
            f"(continuing without them): {', '.join(missing)}"
        )

    for name in sorted(found):
        filename = found[name]
        url = upstream_url + filename
        target = OUTPUT_DIR / filename
        print(f"Downloading {name}: {url}")
        urllib.request.urlretrieve(url, target)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
