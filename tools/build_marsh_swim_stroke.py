"""Package generated whole-body swim strokes, retaining the exact registered entry pose.

No anatomical compositing, mirroring or per-pose stretching. One density per facing;
head landmarks register all articulated poses. Historical sheets remain untouched.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, find_objects

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-swim-stroke-v1'
CATALOG = ROOT / 'character/marsh-v2/catalog.json'
REL = '../marsh-swim-stroke-v1/manifest.json'
SETTINGS = {
    'east': ('01', .355, [4, 5, 1, 3, 2]),
    'west': ('01', .355, [1, 2, 3, 4, 5]),
    'north': ('02', .26, [1, 2, 3, 4, 5]),
    'south': ('01', .255, [1, 2, 3, 4, 5]),
}


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')


def resolve(parent, value):
    return ROOT / value[6:] if value.startswith('res://') else (parent / value).resolve()


def head_box(image):
    a = np.asarray(image).astype(float)
    mask = (a[:, :, 3] > 160) & (a[:, :, 0] > a[:, :, 1] * 1.12) & (a[:, :, 1] > a[:, :, 2] * 1.1) & (a[:, :, 0] > 50)
    labels, _ = label(mask)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    y, x = find_objects((labels == sizes.argmax()).astype('uint8'))[0]
    return [x.start, y.start, x.stop, y.stop]


def build(install=False):
    catalog = json.loads(CATALOG.read_text())
    selected = {}
    for relative in catalog['body']:
        if relative == REL:
            continue
        p = resolve(CATALOG.parent, relative)
        manifest = json.loads(p.read_text())
        for state in manifest['states']:
            selected[state['id']] = (p, manifest, state)
    records = {}
    states = []
    cards = []
    review = BASE / 'review'
    review.mkdir(exist_ok=True)
    for direction, (version, density, order) in SETTINGS.items():
        key = 'swim-' + direction
        p, manifest, original = selected[key]
        anchor_path = resolve(p.parent, original['frameFiles'][0])
        anchor = Image.open(anchor_path).convert('RGBA')
        head = head_box(anchor)
        target = ((head[0] + head[2]) / 2, (head[1] + head[3]) / 2)
        source_path = BASE / f'sources/{direction}-{version}.png'
        sheet = Image.open(source_path).convert('RGBA')
        assert sheet.size == (1536, 1024)
        folder = BASE / 'frames' / key
        folder.mkdir(parents=True, exist_ok=True)
        row = []
        first = Image.new('RGBA', (208, 208))
        first.paste(anchor, (0, 0))
        row.append(first)
        registration = []
        for index in order:
            x, y = index % 3 * 512, index // 3 * 512
            cell = (x, y, x + 512, y + 512)
            if direction == 'north' and index == 5:
                cell = (960, 512, 1536, 1024)
            if direction == 'south' and index == 1:
                cell = (448, 0, 1088, 512)
            if direction == 'south' and index == 2:
                cell = (1088, 0, 1536, 512)
            tile = sheet.crop(cell)
            box = head_box(tile)
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            # Remove faint transparent-provider halos before area downsampling.
            a = np.array(tile)
            a[a[:, :, 3] < 128] = 0
            a[:, :, 3] = np.where(a[:, :, 3] >= 128, 255, 0)
            components, _ = label(a[:, :, 3] > 0)
            sizes = np.bincount(components.ravel())
            sizes[0] = 0
            # Explicit cell cuts can include a disconnected edge of a neighbor.
            # Retain the complete, connected selected body, never isolated arm parts.
            a[components != sizes.argmax()] = 0
            tile = Image.fromarray(a)
            scaled = tile.resize((round(tile.width * density), round(tile.height * density)), Image.Resampling.BOX)
            scaled.putalpha(scaled.getchannel('A').point(lambda value: 255 if value >= 128 else 0))
            offset = (round(target[0] - center[0] * density), round(target[1] - center[1] * density))
            visible = scaled.getbbox()
            assert visible[0] + offset[0] > 0 and visible[1] + offset[1] > 0
            assert visible[2] + offset[0] < 208 and visible[3] + offset[1] < 208, (key, index, visible, offset)
            frame = Image.new('RGBA', (208, 208))
            frame.paste(scaled, offset)
            row.append(frame)
            registration.append(dict(cell=cell, sourcePose=index, headBox=box, offset=offset, density=density))
        assert len(row) == 6
        state = copy.deepcopy(original)
        state['frameFiles'] = []
        for index, frame in enumerate(row):
            target_path = folder / f'{index:03}.png'
            frame.save(target_path)
            state['frameFiles'].append(target_path.relative_to(BASE).as_posix())
        # Same 720 ms cycle and distance-driven stride; more distinct drawings.
        assert sum(original['frameDurationsMs']) == 720
        state['frameDurationsMs'] = [120] * 6
        for name in ['facings', 'waterKinds', 'waterPoses', 'depthOffsets']:
            assert all(v == original[name][0] for v in original[name])
            state[name] = [original[name][0]] * 6
        states.append(state)
        records[key] = dict(source=source_path.relative_to(ROOT).as_posix(), sourceSha256=hashlib.sha256(source_path.read_bytes()).hexdigest(), anchor=anchor_path.relative_to(ROOT).as_posix(), anchorSha256=hashlib.sha256(anchor_path.read_bytes()).hexdigest(), targetHead=target, registration=registration)
        panels = []
        for frame in row:
            panel = Image.new('RGB', (312, 312), '#26333c')
            big = frame.resize((312, 312), Image.Resampling.NEAREST)
            panel.paste(big, (0, 0), big)
            panels.append(panel)
        panels[0].save(review / (key + '.webp'), save_all=True, append_images=panels[1:], duration=[120] * 6, loop=0, lossless=True)
        prior = [Image.open(resolve(p.parent, value)).convert('RGBA') for value in original['frameFiles']]
        comparison = []
        for t in range(0, 720, 60):
            panel = Image.new('RGB', (624, 350), '#26333c')
            draw = ImageDraw.Draw(panel)
            draw.text((12, 10), direction.upper() + ' | Before', fill='white')
            draw.text((324, 10), 'After | pull, recover, extend', fill='white')
            for x, image in [(0, prior[t // 180]), (312, row[t // 120])]:
                big = image.resize((round(image.width * 1.5), round(image.height * 1.5)), Image.Resampling.NEAREST)
                panel.paste(big, (x, 28), big)
            comparison.append(panel)
        comparison[0].save(review / (key + '-comparison.webp'), save_all=True, append_images=comparison[1:], duration=[60] * 12, loop=0, lossless=True)
        cards.append('<article><h2>' + direction.title() + '</h2><img src="' + key + '-comparison.webp"><p><a href="../../../output/marsh-swim-stroke-2026-10-14/native/' + key + '.png">Native holds at 1x and 0.5x</a></p></article>')
        board = Image.new('RGB', (1248, 240), '#26333c')
        for i, frame in enumerate(row):
            board.paste(frame, (i * 208, 20), frame)
        board.save(review / (key + '.png'))
    write(BASE / 'manifest.json', dict(revision='marsh-swim-stroke-v1', frameWidth=208, frameHeight=208, pivot=[92, 172], standingHeight=148, textureFilter='nearest', states=states))
    write(BASE / 'provenance.json', dict(method='Whole generated bodies; explicit cell extraction, one uniform density per direction, head registration, alpha threshold, exact unchanged registered slot 0. No arm cutouts, mirroring, retiming of total cycle, or pose stretching.', frames=records, rejected={'north-01.png': 'Excessively elongated body relative to installed foreshortened pose.'}))
    (review / 'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Marsh swimming strokes</title><style>body{background:#17232b;color:#eeeadd;font:18px system-ui;max-width:1350px;margin:30px auto;padding:0 20px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(570px,1fr));gap:20px}article{background:#26333c;padding:12px}h2{font-size:20px}img{width:100%;image-rendering:pixelated}a{color:#a2d9cc}</style><h1>Marsh swimming strokes</h1><p>Four directions, six poses per cycle. Left: prior loop. Right: revised stroke. Both run for 720 ms. The exact registered first pose preserves the repaired turn handoffs.</p><p>Lossless authored-hold previews; native pose boards below. Natural station travel and a new release export are separate.</p><main>' + ''.join(cards) + '</main>', encoding='utf-8')
    if install and REL not in catalog['body']:
        catalog['body'].append(REL)
        write(CATALOG, catalog)
    print('Marsh swim stroke: 4 cycles / 24 holds, ' + ('installed' if install else 'staged'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true')
    build(parser.parse_args().install)
