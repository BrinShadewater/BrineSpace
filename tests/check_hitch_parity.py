"""Compare native captures after running test_hitch_parity.gd."""
from pathlib import Path
import json
from PIL import Image, ImageChops

root = Path(__file__).resolve().parents[1] / 'output'
records = []
for state in ('q0', 'q1', 'q2', 'q3', 'close', 'rotate-live', 'power-on', 'power-off', 'light-fade', 'raised-walls', 'place', 'remove', 'door-open', 'door-close', 'cull', 'pan', 'zoom') + tuple(f'motion-{q}-{tick}' for q in range(4) for tick in range(3)) + tuple(f'busy-{frame}' for frame in (19,59,99,159)):
    direct = Image.open(root / f'hitch-parity-{state}-direct.png').convert('RGBA')
    cached = Image.open(root / f'hitch-parity-{state}-cached.png').convert('RGBA')
    assert direct.size == cached.size, state
    # RGBA getbbox() may examine only alpha; compare extrema of every channel.
    maximum = max(high for low, high in ImageChops.difference(direct, cached).getextrema())
    records.append({'state': state, 'pixel_identical': maximum == 0,
                    'max_channel_difference': maximum, 'size': direct.size})
(root / 'hitch-pixel-comparison.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
assert all(record['pixel_identical'] for record in records), records
print('HITCH PIXEL PARITY PASS: all four channels identical in all captures')
