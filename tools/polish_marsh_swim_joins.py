"""Share complete selected swim drawings at turns; no generation or pixel retouching.

Run with --install to append the scoped override. Historical sources stay intact.
The input selection excludes this override, making repeated builds deterministic.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-swim-joins-v1'
CATALOG = ROOT / 'character/marsh-v2/catalog.json'
RELATIVE = '../marsh-swim-joins-v1/manifest.json'


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def build(install=False):
    catalog = json.loads(CATALOG.read_text())
    selected = {}
    for relative in catalog['body']:
        if relative in (RELATIVE, '../marsh-swim-stroke-v1/manifest.json'):
            continue
        path = (CATALOG.parent / relative).resolve()
        manifest = json.loads(path.read_text())
        for state in manifest['states']:
            selected[state['id']] = (path, manifest, state)
    BASE.mkdir(parents=True, exist_ok=True)
    sources = {}

    def load_frame(key, index):
        path, manifest, state = selected[key]
        assert manifest['pivot'] == [92, 172] and manifest['standingHeight'] == 148
        source = (path.parent / state['frameFiles'][index]).resolve()
        sources[source.relative_to(ROOT).as_posix()] = hashlib.sha256(source.read_bytes()).hexdigest()
        return Image.open(source).convert('RGBA')

    # An already selected, coherent whole body replaces the doubled-head loop pose.
    north = load_frame('swim-turn-east-north', -1)
    assert north.getbbox()[3] <= 184
    north.crop((0, 0, 184, 184)).save(BASE / 'swim-north-000.png')
    states = []
    loop = copy.deepcopy(selected['swim-north'][2])
    loop['frameFiles'] = [os.path.relpath((selected['swim-north'][0].parent / f).resolve(), BASE).replace('\\', '/') for f in loop['frameFiles']]
    loop['frameFiles'][0] = 'swim-north-000.png'
    states.append(loop)
    for direction in ['east', 'west', 'north', 'south']:
        image = north if direction == 'north' else load_frame('swim-' + direction, 0)
        anchor = Image.new('RGBA', (184, 208))
        anchor.paste(image, (0, 0))
        anchor.save(BASE / ('anchor-' + direction + '.png'))
    for key, (path, manifest, state) in selected.items():
        if not key.startswith('swim-turn-'):
            continue
        origin, destination = key.removeprefix('swim-turn-').split('-')
        revised = copy.deepcopy(state)
        revised['frameFiles'] = [os.path.relpath((path.parent / f).resolve(), BASE).replace('\\', '/') for f in state['frameFiles']]
        revised['frameFiles'][0] = 'anchor-' + origin + '.png'
        revised['frameFiles'][-1] = 'anchor-' + destination + '.png'
        states.append(revised)
    assert len(states) == 13
    write_json(BASE / 'manifest.json', dict(revision='marsh-swim-joins-v1', pivot=[92, 172], standingHeight=148, textureFilter='nearest', states=states))
    write_json(BASE / 'provenance.json', dict(
        sources=sources,
        method='Whole selected north turn endpoint reused for north loop slot 0. Complete swim slot 0 drawings shared at all 12 turn entries/exits; transparent bottom padding only. No generated artwork, anatomical compositing, grading or retiming.',
        preserved='All interior turn drawings, remaining loop slots, timing, facing, water and depth metadata; all unrelated selections.',
        changedStates=[s['id'] for s in states]))
    if install and RELATIVE not in catalog['body']:
        catalog['body'].append(RELATIVE)
        write_json(CATALOG, catalog)
    print('Marsh swim joins: 13 states, 5 packaged PNGs; ' + ('installed' if install else 'built'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true')
    build(parser.parse_args().install)
