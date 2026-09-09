"""Read-only, hash-bound checks of selected transparent and opaque asset pixels.

This checks named points, not the whole silhouette or visual acceptance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def local_file(root, value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Expected a local file path')
    path = (root / value.removeprefix('res://')).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('File must exist inside the project')
    return path


def check(root, record_path):
    record = local_file(root, str(record_path))
    data = json.loads(record.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Probe record must be an object')
    export = local_file(root, data.get('export_path'))
    digest = hashlib.sha256(export.read_bytes()).hexdigest()
    if digest != data.get('export_sha256'):
        raise ValueError('Export hash mismatch; re-review changed art')
    if data.get('coordinate_space') != 'original native canvas pixels':
        raise ValueError('Unsupported coordinate space')
    with Image.open(export) as image:
        if 'A' not in image.getbands():
            raise ValueError('Export needs an explicit alpha channel')
        if data.get('native_canvas_px') != list(image.size):
            raise ValueError('Native canvas mismatch')
        probes = data.get('probes')
        if not isinstance(probes, list) or not probes:
            raise ValueError('At least one probe is required')
        names, coordinates, results = set(), set(), []
        alpha = image.getchannel('A')
        for probe in probes:
            if not isinstance(probe, dict):
                raise ValueError('Probe must be an object')
            name, at = probe.get('name'), probe.get('at')
            if not isinstance(name, str) or not name.strip() or name in names:
                raise ValueError('Probe names must be nonempty and unique')
            names.add(name)
            if (not isinstance(at, list) or len(at) != 2
                    or any(type(v) is not int for v in at)
                    or not (0 <= at[0] < image.width and 0 <= at[1] < image.height)):
                raise ValueError(f'{name}: coordinate outside native canvas or not integer')
            if tuple(at) in coordinates:
                raise ValueError(f'{name}: duplicate probe coordinate')
            coordinates.add(tuple(at))
            expected = probe.get('expected')
            if expected not in ('transparent', 'opaque'):
                raise ValueError(f'{name}: expected must be transparent or opaque')
            actual = alpha.getpixel(tuple(at))
            target = 0 if expected == 'transparent' else 255
            if actual != target:
                raise ValueError(f'{name}: expected alpha {target}, found {actual}')
            if type(probe.get('alpha')) is not int or probe['alpha'] != actual:
                raise ValueError(f'{name}: recorded alpha does not match current pixel')
            results.append({'name': name, 'at': at, 'alpha': actual})
    return {'export_sha256': digest, 'checked': len(results), 'probes': results,
            'scope': 'Selected pixels only; no silhouette, placement or visual acceptance'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', help='Project-local alpha probe JSON')
    args = parser.parse_args()
    try:
        result = check(ROOT, args.record)
    except (ValueError, OSError, TypeError) as error:
        print(f'ALPHA PROBES FAILED: {error}', file=sys.stderr)
        return 1
    print(f"ALPHA PROBES PASS: {result['checked']} hash-bound pixels; selected points only")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
