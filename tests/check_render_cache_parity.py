"""Compare native captures after running test_render_cache_parity.gd."""
from pathlib import Path
import json
from PIL import Image, ImageChops

root = Path(__file__).resolve().parents[1] / 'output'
records = []
for state in ('q0', 'q1', 'q2', 'q3', 'close'):
    direct = Image.open(root / f'render-parity-{state}-direct.png').convert('RGBA')
    cached = Image.open(root / f'render-parity-{state}-cached.png').convert('RGBA')
    assert direct.size == cached.size, state
    # RGBA getbbox() may examine only alpha; compare extrema of every channel.
    maximum = max(high for low, high in ImageChops.difference(direct, cached).getextrema())
    records.append({'state': state, 'pixel_identical': maximum == 0,
                    'max_channel_difference': maximum, 'size': direct.size})
(root / 'render-pixel-comparison.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
assert all(record['pixel_identical'] for record in records), records
print('RENDER PIXEL PARITY PASS: all four channels identical in five captures')
