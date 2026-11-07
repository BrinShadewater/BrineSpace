"""Reconstruct Bill's south action repair from preserved authored sheets."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image

SOURCE = Path('character/major-bill-v3/sources/south-actions-2026-09-21')


def extract(source, spec):
    pixels = np.array(source)
    pixels[pixels[:, :, 3] < 128] = 0
    pixels[pixels[:, :, 3] >= 128, 3] = 255
    source = Image.fromarray(pixels)
    frames = []
    for box in spec['boxes']:
        crop = source.crop(box)
        crop = crop.resize((round(crop.width * spec['scale']), round(crop.height * spec['scale'])), Image.Resampling.NEAREST)
        frame = Image.new('RGBA', (256, 256))
        frame.alpha_composite(crop, (128 - crop.width // 2, 224 - crop.height))
        frames.append(frame)
    return frames


def build(root, read, image, helmet, tilted):
    """Return bare/equipped clips; callbacks retain canonical provenance tracking."""
    source = root / SOURCE
    spec = read(source / 'registration.json')
    work_spec = read(source / 'repair-registration.json')
    for name, metadata in [('generated-source.png', spec), ('repair-source.png', work_spec)]:
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != metadata['source_sha256']:
            raise ValueError('Bill south action source changed: ' + name)
    kneel = extract(image(source / 'generated-source.png'), spec)
    correction = read(source / 'footlock-registration.json')
    index = correction['frame']
    original = np.array(kneel[index])
    pixels = original.copy()
    yy, xx = np.mgrid[:256, :256]
    x0, y0, x1, y1 = correction['region']
    start, end = correction['ramp_y']
    shift = np.rint(-correction['x_shift'] * np.clip((yy - start) / (end - start), 0, 1)).astype(int)
    srcx = xx + shift
    region = (xx >= x0) & (xx < x1) & (yy >= y0) & (yy < y1)
    pixels[region] = original[yy[region], srcx[region]]
    pixels[region & (srcx >= x1)] = 0
    kneel[index] = Image.fromarray(pixels)
    registered = extract(image(source / 'repair-source.png'), work_spec)
    repair = []
    rect = tuple(work_spec['replacement_region'])
    for i, frame in enumerate(registered):
        pose = kneel[-1].copy()
        if i not in [0, 5]:
            pose.paste(frame.crop(rect), rect)
        repair.append(pose)
    bare = {'kneel-south': kneel, 'repair-south': repair, 'stand-south': list(reversed(kneel))}
    fit = read(source / 'helmet-registration.json')
    anchors = {(r['folder'], r['frame']): np.array(r['head']) for r in fit['head_anchors']}
    overlay = helmet.overlay('front', tuple(fit['overlay_size']))
    equipped = {}
    for action, folder in [('kneel-south', 'footlock-candidate'), ('repair-south', 'repair-candidate')]:
        poses = []
        for i, body in enumerate(bare[action]):
            head = anchors[folder, i]
            poses.append(tilted(body, overlay, head - np.array(fit['overlay_anchor_offset']), 0, [*(head - [14, 20]), 28, 34], 'south'))
        equipped[action] = poses
    equipped['stand-south'] = list(reversed(equipped['kneel-south']))
    return bare, equipped
