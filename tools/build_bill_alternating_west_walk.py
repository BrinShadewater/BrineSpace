"""Reproduce the selected alternating west walk from reviewed frozen sources."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image, ImageFilter

SOURCE = Path('character/major-bill-v3/sources/west-walk-alternation-2026-09-21')


def build(root, read, image, helmet, tilted, verify_equipment=True):
    source = root / SOURCE
    spec = read(source / 'walk-registration.json')
    surface = root / spec['surface']['source']
    if hashlib.sha256(surface.read_bytes()).hexdigest() != spec['surface']['sha256']:
        raise ValueError('Bill west surface source changed')
    atlas = image(surface).resize((552, 368), Image.Resampling.LANCZOS)
    overlay = helmet.overlay('west', (48, 56))
    bodies, equipped = [], []
    for index, pose in enumerate(spec['frames']):
        path = source / pose['source']
        if hashlib.sha256(path.read_bytes()).hexdigest() != pose['sha256']:
            raise ValueError('Bill west pose source changed: ' + pose['source'])
        raw = image(path)
        raw.putalpha(raw.getchannel('A').point(lambda a: 0 if a <= 16 else a))
        scale = pose['scale']
        raw = raw.resize((round(raw.width * scale), round(raw.height * scale)), Image.Resampling.LANCZOS)
        body = Image.new('RGBA', (184, 184))
        body.alpha_composite(raw, tuple(pose['destination']))
        pixels = np.array(body)
        interior = np.array(body.getchannel('A').filter(ImageFilter.MinFilter(3))) >= 250
        mask = interior & (np.indices(interior.shape)[0] >= 122)
        x, y = index % 3 * 184, index // 3 * 184
        detail = np.array(atlas.crop((x, y, x + 184, y + 184)))
        pixels[mask, :3] = detail[mask, :3]
        transparent = pixels[:, :, 3] < 128
        pixels[transparent] = 0
        pixels[~transparent, 3] = 255
        body = Image.fromarray(pixels)
        head = np.array(spec['helmet'][index]['head'])
        fitted = tilted(body, overlay, head - [23, 25], 0,
                        [*(head - [14, 20]), 28, 34], 'west')
        for variant, frame in [('bare', body), ('helmet', fitted)]:
            if variant=='helmet' and not verify_equipment:continue
            if hashlib.sha256(frame.tobytes()).hexdigest() != spec['expected_rgba'][variant][index]:
                raise ValueError('Bill west candidate recipe drift: %s/%d' % (variant, index))
        bodies.append(body)
        equipped.append(fitted)
    return {'walk-west': bodies}, {'walk-west': equipped}
