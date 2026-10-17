"""Supporting measurements for visual review; not an art-acceptance gate."""
from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
states = {s['id']: s for s in manifest['states']}
rows = []
for heading, meta in manifest['headings'].items():
    pose = Image.open(ROOT / meta['pose']).convert('RGBA')
    pixels = np.asarray(pose).astype(float)
    opaque = pixels[:, :, 3] > 245
    cyan = opaque & (pixels[:, :, 1] - pixels[:, :, 0] > 20) & (pixels[:, :, 2] - pixels[:, :, 0] > 20)
    drive = np.asarray(Image.open(ROOT / states['drive-' + heading]['frameFiles'][0]).convert('RGBA')).astype(float)
    delta = np.max(np.abs(drive[:, :, :3] - pixels[:, :, :3]), axis=2)
    bbox = pose.getbbox()
    rows.append({
        'heading': heading,
        'boundsLibraryPixels': [bbox[2]-bbox[0], bbox[3]-bbox[1]],
        'boundsWorldUnits': [round((bbox[2]-bbox[0])*.34, 2), round((bbox[3]-bbox[1])*.34, 2)],
        'cyanMaskPercentOpaque': round(100 * cyan.sum() / opaque.sum(), 2),
        'cyanMeanChannelSpread': round(float((pixels[:,:,:3].max(axis=2)-pixels[:,:,:3].min(axis=2))[cyan].mean()), 2) if cyan.any() else None,
        'driveFrameZeroChangedOpaquePixelsOver8': int(((delta > 8) & opaque).sum()),
        'driveFrameZeroAlphaMatchesPose': bool(np.array_equal(drive[:,:,3], pixels[:,:,3])),
    })
report = {'purpose': 'Supporting measurements, not visual acceptance. Axis-aligned bounds vary naturally with heading; cyan mask is an approximate chroma diagnostic.', 'headings': rows}
(ROOT / 'review/art-audit-metrics.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
for row in rows:
    print(row['heading'], row['boundsWorldUnits'], 'cyan%', row['cyanMaskPercentOpaque'], 'start texture pixels', row['driveFrameZeroChangedOpaquePixelsOver8'])
