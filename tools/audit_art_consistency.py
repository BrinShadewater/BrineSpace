"""Read-only raster inventory and palette diagnostics, not visual acceptance.

Run: python tools/audit_art_consistency.py --output output/art-consistency
Source/revision images are counted separately from explicit consumer references.
Animation frames are inventoried individually; their aesthetic review is by family.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import csv
import hashlib
import json
import re
import subprocess

from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {'.png', '.webp', '.jpg', '.jpeg', '.gif'}


def inventory(output):
    raw = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT)
    names = sorted(set(p for p in raw.decode().split('\0') if p and Path(p).suffix.lower() in EXTENSIONS))
    refs = set()
    for directory in ['scripts', 'scenes', 'rooms', 'assets', 'brineui']:
        for path in (ROOT / directory).rglob('*'):
            if path.suffix not in {'.gd', '.tscn', '.tres'}:
                continue
            refs.update(re.findall(r'res://([^"\n]+\.(?:png|webp|jpg|jpeg|gif))', path.read_text(encoding='utf-8', errors='replace')))

    def inspect(name):
        path = ROOT / name
        family = '/'.join(path.relative_to(ROOT).parts[:2])
        result = {'path': name, 'family': family, 'explicit_consumer_reference': name in refs}
        try:
            with Image.open(path) as original:
                result.update(width=original.width, height=original.height, mode=original.mode)
                sample = original.convert('RGBA')
                sample.thumbnail((96, 96), Image.Resampling.NEAREST)
                arr = np.asarray(sample).astype(np.float64) / 255.0
                mask = arr[:, :, 3] > 0.9
                pixels = arr[:, :, :3][mask]
                if len(pixels):
                    bright = pixels.max(axis=1)
                    saturation = (bright - pixels.min(axis=1)) / np.maximum(bright, .001)
                    luminance = pixels @ np.array([.2126, .7152, .0722])
                    result.update(mean_luminance=round(float(luminance.mean()), 4),
                                  p95_luminance=round(float(np.quantile(luminance, .95)), 4),
                                  mean_saturation=round(float(saturation.mean()), 4),
                                  pale_highlight_fraction=round(float(((luminance > .85) & (saturation < .2)).mean()), 4),
                                  vivid_fraction=round(float(((saturation > .7) & (bright > .6)).mean()), 4))
                result['alpha_sample_fraction'] = round(float((arr[:, :, 3] < 1).mean()), 4)
            result['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        except Exception as error:
            result['error'] = str(error)
        return result

    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(inspect, names))
    output.mkdir(parents=True, exist_ok=True)
    (output / 'raster-inventory.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    fields = sorted(set().union(*(r.keys() for r in records)))
    with (output / 'raster-inventory.csv').open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    summary = {'raster_files': len(records), 'families': len(set(r['family'] for r in records)),
               'explicit_consumer_references': sum(r['explicit_consumer_reference'] for r in records),
               'decode_errors': [r for r in records if 'error' in r],
               'scope': 'All Git-visible rasters, including source/history. References are static hints; dynamic consumers and visual acceptance require native review.'}
    (output / 'inventory-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'output/art-consistency')
    inventory(parser.parse_args().output)
