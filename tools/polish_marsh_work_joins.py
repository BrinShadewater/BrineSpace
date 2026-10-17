"""Reuse current whole south idle at torch entry/exit; preserve all work interiors."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-work-joins-v1'
CATALOG = ROOT / 'character/marsh-v2/catalog.json'
OVERRIDE = '../marsh-work-joins-v1/manifest.json'


def resolve(parent, path):
    return ROOT / path[6:] if path.startswith('res://') else (parent / path).resolve()


def selection():
    result = {}
    for relative in json.loads(CATALOG.read_text())['body']:
        if relative == OVERRIDE:
            continue
        p = resolve(CATALOG.parent, relative)
        m = json.loads(p.read_text())
        for state in m['states']:
            result[state['id']] = (p, m, state)
    return result


def build(install=False):
    selected = selection()
    p, m, idle = selected['idle-south']
    source = resolve(p.parent, idle['frameFiles'][0])
    body = Image.open(source).convert('RGBA')
    BASE.mkdir(exist_ok=True)
    states, changes = [], []
    for key, slot in [('torch-draw-south', 0), ('torch-stow-south', 5)]:
        old_path, old_meta, old = selected[key]
        original = resolve(old_path.parent, old['frameFiles'][slot])
        old_image = Image.open(original).convert('RGBA')
        assert old_meta['standingHeight'] == m['standingHeight'] == 148
        offset = tuple(round(a-b) for a, b in zip(old_meta['pivot'], m['pivot']))
        revised = Image.new('RGBA', old_image.size)
        bounds = body.getbbox()
        assert bounds[0]+offset[0] >= 0 and bounds[1]+offset[1] >= 0
        assert bounds[2]+offset[0] <= revised.width and bounds[3]+offset[1] <= revised.height
        revised.paste(body, offset)
        revised.save(BASE / 'idle-south-padded.png')
        state = copy.deepcopy(old)
        state['frameFiles'] = ['res://' + resolve(old_path.parent, f).relative_to(ROOT).as_posix() for f in old['frameFiles']]
        state['frameFiles'][slot] = 'res://character/marsh-work-joins-v1/idle-south-padded.png'
        states.append(state)
        changes.append(dict(state=key, slot=slot, previous=original.relative_to(ROOT).as_posix(),
                            previousSha256=hashlib.sha256(original.read_bytes()).hexdigest(), offset=offset))
        if len(states) == 1:
            manifest = copy.deepcopy(old_meta)
        else:
            assert all(manifest[k] == old_meta[k] for k in ['pivot', 'standingHeight', 'frameWidth', 'frameHeight'])
    manifest.update(revision='marsh-south-torch-idle-joins-v1', states=states)
    (BASE / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (BASE / 'provenance.json').write_text(json.dumps(dict(
        source=source.relative_to(ROOT).as_posix(), sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        method='Exact whole selected south idle, registered by existing pivot and transparent padding only.',
        changedSlots=changes, preserved='All interior drawings, welding loop, authored clocks, density, pivot, controller and other states.'), indent=2)+'\n')
    if install:
        catalog = json.loads(CATALOG.read_text())
        if OVERRIDE not in catalog['body']:
            catalog['body'].append(OVERRIDE)
        CATALOG.write_text(json.dumps(catalog, indent=2)+'\n')
    print('South torch joins: two endpoints / one whole idle drawing; ' + ('installed' if install else 'staged'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true')
    build(parser.parse_args().install)
