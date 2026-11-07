"""One masked material calibration from preserved open-pod sources; no resampling."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/cryo-material-pass-v1'

def build():
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for actor in ('bill', 'veld', 'branforth'):
        source = ROOT / f'assets/material-polish-cryo-open-v1/{actor}.png'
        image = Image.open(source).convert('RGBA')
        pixels = np.asarray(image).copy()
        mask = Image.new('L', image.size)
        ImageDraw.Draw(mask).rounded_rectangle((137, 151, 285, 449), radius=16, fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(3))
        weight = np.asarray(mask, dtype=float)[:, :, None] / 255
        # Only neutral padded upholstery: preserve glass, cream shell, hardware,
        # lamp, alpha and registration. Apply once from the immutable source.
        rgb = pixels[:, :, :3].astype(float)
        pixels[:, :, :3] = np.rint(rgb * (1 - weight + weight * np.array([.78, .85, .91]))).astype('uint8')
        result = Image.fromarray(pixels)
        result.save(OUT / f'{actor}-open.png')
        mask.save(OUT / f'{actor}-upholstery-mask.png')
        assert np.array_equal(pixels[:, :, 3], np.asarray(image)[:, :, 3])
        assert np.array_equal(pixels[np.asarray(mask) == 0], np.asarray(image)[np.asarray(mask) == 0])
        records.append({'actor': actor, 'source': str(source.relative_to(ROOT)),
                        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                        'output_sha256': hashlib.sha256((OUT / f'{actor}-open.png').read_bytes()).hexdigest()})
    (OUT / 'registration.json').write_text(json.dumps({
        'canvas': [418, 627], 'pivot': [210, 560], 'resampling': 'none',
        'material': 'neutral padded upholstery only', 'rgbMultiplier': [.78, .85, .91],
        'mask': {'roundedBounds': [137, 151, 285, 449], 'radius': 16, 'feather': 3},
        'sources': records, 'unchanged': ['alpha', 'shell', 'glass', 'hardware', 'lamp', 'geometry']
    }, indent=2) + '\n')
    print('Built three registered material-calibrated open pods; alpha and unmasked pixels exact.')

if __name__ == '__main__':
    build()
