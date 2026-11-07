"""Rebuild south work from canonical-identity sources and exact idle endpoints."""
from pathlib import Path
import hashlib
import numpy as np
from PIL import Image, ImageDraw
from build_bill_west_style_actions import solid

SOURCE = Path('character/major-bill-v3/sources/south-actions-style-2026-09-21')


def build(root, read, image, helmet, tilted, idle_equipment=None):
    source = root / SOURCE
    spec = read(source / 'candidate-registration.json')
    for name, digest in spec['source_hashes'].items():
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Bill south style source changed: ' + name)
    raw = solid(image(source / 'lowering-source.png'))
    kneel = []
    for row in spec['lowering']['frames']:
        crop = raw.crop(row['box'])
        scale = spec['lowering']['scale']
        crop = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.NEAREST)
        frame = Image.new('RGBA', (256, 256))
        frame.alpha_composite(crop, tuple(row['paste']))
        kneel.append(frame)
    idle = {}
    for variant in ('bare', 'helmet'):
        idle[variant] = Image.new('RGBA', (256, 256))
        idle[variant].alpha_composite(image(source / f'{variant}-idle-reference.png'), (36, 52))
    if idle_equipment is not None:
        idle['helmet']=Image.new('RGBA',(256,256))
        idle['helmet'].alpha_composite(idle_equipment,(36,52))
    kneel[0] = idle['bare']
    work = spec['work']
    mask = Image.new('L', (256, 256))
    ImageDraw.Draw(mask).polygon([tuple(p) for p in work['replacement_polygon']], fill=255)
    raw = solid(image(source / 'work-source.png'))
    repair = []
    for index in range(6):
        frame = kneel[-1].copy()
        if index not in (0, 5):
            width = work['cell_width']
            crop = raw.crop((index * width, 0, (index + 1) * width, raw.height))
            crop = crop.resize((round(crop.width * work['scale']), round(crop.height * work['scale'])), Image.Resampling.NEAREST)
            registered = Image.new('RGBA', (256, 256))
            registered.alpha_composite(crop, tuple(work['paste']))
            frame.paste(registered, (0, 0), mask)
        repair.append(frame)
    bare = {'kneel-south': kneel, 'repair-south': repair, 'stand-south': list(reversed(kneel))}
    overlay = helmet.overlay('front', tuple(spec['overlay_size']))
    equipped = {}
    for action in ('kneel-south', 'repair-south'):
        heads = spec['head_anchors'] if action.startswith('kneel') else [spec['head_anchors'][-1]] * 6
        equipped[action] = []
        for frame, anchor in zip(bare[action], heads):
            head = np.array(anchor)
            equipped[action].append(tilted(frame, overlay, head - np.array(spec['overlay_anchor_offset']), 0,
                                           [*(head - [14, 20]), 28, 34], 'south'))
    equipped['kneel-south'][0] = idle['helmet']
    equipped['stand-south'] = list(reversed(equipped['kneel-south']))
    return bare, equipped
