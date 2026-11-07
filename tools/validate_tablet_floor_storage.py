#!/usr/bin/env python3
"""Reject stale derived iPad floor resources before export; never changes artwork."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate(root=ROOT):
    manifest = json.loads((root / 'assets/tablet-floor-vram/manifest.json').read_text())
    problems = []
    for row in manifest['textures']:
        for field, digest in [('source', 'source_sha256'), ('resource', 'resource_sha256')]:
            path = row[field]
            relative = Path(path.removeprefix('res://'))
            if not path.startswith('res://') or relative.is_absolute() or '..' in relative.parts:
                problems.append('Invalid asset path: ' + path)
                continue
            local = root / relative
            if not local.is_file():
                problems.append('Missing tablet floor storage input: ' + path)
                continue
            data = local.read_bytes()
            if data.startswith(b'version https://git-lfs.github.com/spec/'):
                problems.append('Fetch Git LFS artwork before exporting: ' + path)
            elif hashlib.sha256(data).hexdigest() != row[digest]:
                problems.append('Rebake tablet floor storage; changed ' + path)
    return problems

if __name__ == '__main__':
    errors = validate()
    for error in errors:
        print('PENDING: ' + error)
    if not errors:
        print('TABLET FLOOR STORAGE: source and derived resource hashes match.')
    raise SystemExit(2 if errors else 0)
