"""Reproduce the selected alternating east walk from reviewed frozen sources."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image

SOURCE = Path('character/major-bill-v3/sources/east-walk-alternation-2026-09-21')


def build(root, read, image, helmet, tilted, verify_equipment=True):
    source = root / SOURCE
    spec = read(source / 'walk-registration.json')
    overlay = helmet.overlay('east', (46, 56))
    bodies, equipped = [], []
    for index, pose in enumerate(spec['frames']):
        path = source / pose['source']
        if hashlib.sha256(path.read_bytes()).hexdigest() != pose['sha256']:
            raise ValueError('Bill east pose source changed: ' + pose['source'])
        pixels = np.array(image(path))
        transparent = pixels[:, :, 3] < 128
        pixels[transparent] = 0
        pixels[~transparent, 3] = 255
        raw = Image.fromarray(pixels)
        scale = pose['scale']
        raw = raw.resize((round(raw.width * scale), round(raw.height * scale)), Image.Resampling.LANCZOS)
        body = Image.new('RGBA', (184, 184))
        body.alpha_composite(raw, tuple(pose['destination']))
        pixels = np.array(body)
        transparent = pixels[:, :, 3] < 128
        pixels[transparent] = 0
        pixels[~transparent, 3] = 255
        body = Image.fromarray(pixels)
        head = np.array(spec['helmet'][index]['head'])
        fitted = tilted(body, overlay, head - [26, 24], 0,
                        [*(head - [14, 20]), 28, 34], 'east')
        for variant, frame in [('bare', body), ('helmet', fitted)]:
            if variant=='helmet' and not verify_equipment:continue
            if hashlib.sha256(frame.tobytes()).hexdigest() != spec['expected_rgba'][variant][index]:
                raise ValueError('Bill east reviewed recipe drift: %s/%d' % (variant, index))
        bodies.append(body)
        equipped.append(fitted)
    return {'walk-east': bodies}, {'walk-east': equipped}
