"""Rebuild connected west work poses from the canonical-identity source study."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image, ImageDraw

SOURCE = Path('character/major-bill-v3/sources/west-actions-style-2026-09-21')


def solid(image):
    pixels = np.array(image.convert('RGBA'))
    pixels[pixels[:, :, 3] < 128] = 0
    pixels[pixels[:, :, 3] >= 128, 3] = 255
    return Image.fromarray(pixels)


def build(root, read, image, helmet, tilted):
    source = root / SOURCE
    lowering = read(source / 'lowering-registration.json')
    work = read(source / 'work-registration.json')
    for filename, spec in [('lowering-source.png', lowering), ('work-source.png', work)]:
        if hashlib.sha256((source / filename).read_bytes()).hexdigest() != spec['sha256']:
            raise ValueError('Bill west style source changed: ' + filename)
    raw = solid(image(source / 'lowering-source.png'))
    kneel = []
    for pose in lowering['frames']:
        crop = raw.crop(pose['box'])
        crop = crop.resize((round(crop.width * lowering['scale']), round(crop.height * lowering['scale'])), Image.Resampling.NEAREST)
        frame = Image.new('RGBA', tuple(lowering['canvas']))
        frame.alpha_composite(crop, tuple(pose['paste']))
        kneel.append(frame)
    mask = Image.new('L', (256, 256))
    ImageDraw.Draw(mask).polygon([tuple(point) for point in work['replacement_polygon']], fill=255)
    raw = solid(image(source / 'work-source.png'))
    repair = []
    for index in range(6):
        frame = kneel[-1].copy()
        if index not in (0, 5):
            width = work['cell_width']
            crop = raw.crop((index * width, 0, (index + 1) * width, raw.height))
            crop = crop.resize((round(crop.width * work['scale']), round(crop.height * work['scale'])), Image.Resampling.NEAREST)
            registered = Image.new('RGBA', frame.size)
            registered.alpha_composite(crop, tuple(work['paste']))
            frame.paste(registered, (0, 0), mask)
        repair.append(frame)
    bare = {'kneel-west': kneel, 'repair-west': repair, 'stand-west': list(reversed(kneel))}
    fit = read(source / 'helmet-registration.json')
    anchors = {(row['folder'], row['frame']): np.array(row['head']) for row in fit['head_anchors']}
    overlay = helmet.overlay('west', tuple(fit['overlay_size']))
    equipped = {}
    for action, folder in [('kneel-west', 'contact-candidate'), ('repair-west', 'repair-candidate')]:
        equipped[action] = []
        for index, body in enumerate(bare[action]):
            head = anchors[folder, index]
            equipped[action].append(tilted(body, overlay, head - np.array(fit['overlay_anchor_offset']), 0,
                                          [*(head - [14, 20]), 28, 34], 'west'))
    equipped['stand-west'] = list(reversed(equipped['kneel-west']))
    return bare, equipped
