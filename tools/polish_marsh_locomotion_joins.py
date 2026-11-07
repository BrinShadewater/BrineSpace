"""Reuse selected whole standing/gait bodies at nine locomotion boundaries.

Keeps authored timing, pivots, canvas sizes, root curves and all interior poses.
No painting, resampling, generation, mirroring or anatomical fitting.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-locomotion-joins-v1'
CATALOG = ROOT / 'character/marsh-v2/catalog.json'
OVERRIDES = ['../marsh-locomotion-joins-v1/manifest-p128-224.json', '../marsh-locomotion-joins-v1/manifest-p92-172.json']


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def resolve(parent, relative):
    return ROOT / relative[6:] if relative.startswith('res://') else (parent / relative).resolve()


def build(install=False):
    catalog = json.loads(CATALOG.read_text())
    selected = {}
    for relative in catalog['body']:
        if relative in OVERRIDES:
            continue
        p = resolve(CATALOG.parent, relative)
        manifest = json.loads(p.read_text())
        for state in manifest['states']:
            selected[state['id']] = (p, manifest, state)
    BASE.mkdir(exist_ok=True)
    changes = []
    groups = {}
    repairs = {}
    for direction in ['east', 'west']:
        repairs['walk-start-' + direction] = [(0, 'idle-' + direction, 0)]
        repairs['walk-stop-' + direction] = [(-1, 'idle-' + direction, 0)]
        repairs['walk-step-' + direction] = [(0, 'idle-' + direction, 0), (-1, 'idle-' + direction, 0)]
    repairs['walk-start-north'] = [(-1, 'walk-north', 1)]
    for key, edits in repairs.items():
        path, metadata, original = selected[key]
        state = copy.deepcopy(original)
        state['frameFiles'] = [os.path.relpath(resolve(path.parent, f), BASE).replace('\\', '/') for f in state['frameFiles']]
        pivot = tuple(metadata['pivot'])
        for index, authority, slot in edits:
            source_manifest, source_metadata, source_state = selected[authority]
            source = resolve(source_manifest.parent, source_state['frameFiles'][slot])
            prior = resolve(path.parent, original['frameFiles'][index])
            old = Image.open(prior).convert('RGBA')
            body = Image.open(source).convert('RGBA')
            assert metadata['standingHeight'] == source_metadata['standingHeight'] == 148
            source_pivot = source_metadata['pivot']
            offset = (round(pivot[0] - source_pivot[0]), round(pivot[1] - source_pivot[1]))
            bounds = body.getbbox()
            assert min(bounds[0] + offset[0], bounds[1] + offset[1]) > 0
            assert bounds[2] + offset[0] < old.width and bounds[3] + offset[1] < old.height
            frame = Image.new('RGBA', old.size)
            frame.paste(body, offset)
            filename = f'{authority}-{slot:03}-p{pivot[0]}-{pivot[1]}.png'
            frame.save(BASE / filename)
            state['frameFiles'][index] = filename
            changes.append(dict(state=key, slot=index if index >= 0 else len(state['frameFiles']) + index,
                                source=source.relative_to(ROOT).as_posix(), sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                previous=prior.relative_to(ROOT).as_posix(), previousSha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
                                output=filename, offset=offset))
        groups.setdefault(pivot, [copy.deepcopy(metadata), []])[1].append(state)
    for pivot, (metadata, states) in groups.items():
        metadata['revision'] = 'marsh-locomotion-joins-v1'
        metadata['states'] = states
        write(BASE / f'manifest-p{pivot[0]}-{pivot[1]}.json', metadata)
    write(BASE / 'provenance.json', dict(method='Selected complete bodies copied at their original registered pivots. Transparent padding only; no source artwork overwritten. North start hands off into gait slot 1 at controller phase .23.', changedSlots=changes))
    if install:
        for relative in OVERRIDES:
            if relative not in catalog['body']:
                catalog['body'].append(relative)
        write(CATALOG, catalog)
    print('Marsh locomotion joins: 7 states / 9 boundary holds / 3 shared drawings; ' + ('installed' if install else 'staged'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true')
    build(parser.parse_args().install)
