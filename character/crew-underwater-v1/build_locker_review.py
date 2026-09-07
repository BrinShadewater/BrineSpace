"""Build a source-hashed, pivot-registered review of adjacent locker actions."""
from pathlib import Path
import hashlib
import json
import os
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'revisions'
actors = []
for actor, name in [('bill', 'Major Bill'), ('veld', 'Dr. Veld'), ('branforth', 'Chief Engineer Branforth')]:
    clips = []
    paths = [('equip', ROOT / f'pilot/{actor}-equip-helmet-east'), ('remove', ROOT / f'pilot/{actor}-remove-helmet-east')]
    pickup_version = {'bill': 'v4', 'veld': 'v1', 'branforth': 'v2'}[actor]
    paths.insert(0, ('pickup candidate', OUT / f'{actor}-pickup-helmet-east-{pickup_version}'))
    paths.append(('deposit candidate', OUT / f'{actor}-deposit-helmet-east-v1'))
    for label, path in paths:
        manifest = json.loads((path / 'manifest.json').read_text(encoding='utf-8'))
        state = manifest['states'][0]
        assert len(state['frameFiles']) == len(state['frameDurationsMs'])
        frames = []
        for file, duration in zip(state['frameFiles'], state['frameDurationsMs']):
            source = path / file
            with Image.open(source) as image:
                assert image.size == (manifest['frameWidth'], manifest['frameHeight'])
                assert image.convert('RGBA').getbbox() is not None
            assert duration > 0
            frames.append({'url': '../' + source.relative_to(ROOT).as_posix(), 'duration': duration,
                           'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        clips.append({'label': label, 'pivot': manifest['pivot'], 'width': manifest['frameWidth'],
                      'height': manifest['frameHeight'], 'frames': frames, 'events': state.get('events', [])})
    # Preserve stage labels while reviewing the actual composed runtime timing.
    for action, first in [('equip-helmet', 0), ('remove-helmet', 2)]:
        runtime = json.loads((ROOT / f'locker/{actor}-{action}-east/manifest.json').read_text(encoding='utf-8'))['states'][0]
        joined = clips[first]['frames'] + clips[first + 1]['frames']
        assert len(joined) == len(runtime['frameDurationsMs'])
        for frame, duration in zip(joined, runtime['frameDurationsMs']):
            frame['duration'] = duration
    actors.append({'id': actor, 'name': name, 'clips': clips,
                   'missing': [], 'unverified': ['idle/action and stage pose joins', 'held/shelf helmet silhouette match', 'continuous visual acceptance']})
for actor in actors:
    assert actor['clips'][0]['frames'][-1]['sha256'] == actor['clips'][1]['frames'][0]['sha256']
    assert actor['clips'][2]['frames'][-1]['sha256'] == actor['clips'][3]['frames'][0]['sha256']
    character = {'bill': 'major-bill-v2', 'veld': 'dr-veld-v1', 'branforth': 'chief-engineer-branforth-v1'}[actor['id']]
    idles = []
    for equipped in [False, True]:
        path = (ROOT / f'equipment/dry/{actor["id"]}-idle-east/manifest.json' if equipped
                else ROOT.parent / character / 'final/manifest.json')
        manifest = json.loads(path.read_text(encoding='utf-8'))
        state = next(s for s in manifest['states'] if s['id'] == 'idle-east')
        frames = []
        for file, duration in zip(state['frameFiles'], state['frameDurationsMs']):
            source = (path.parent / file).resolve()
            with Image.open(source) as image:
                assert image.size == (manifest['frameWidth'], manifest['frameHeight'])
            frames.append({'url': os.path.relpath(source, OUT).replace('\\', '/'), 'duration': duration,
                           'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        idles.append({'label': 'equipped idle' if equipped else 'bare idle', 'pivot': manifest['pivot'],
                      'width': manifest['frameWidth'], 'height': manifest['frameHeight'], 'frames': frames, 'events': []})
    # Include a full idle cycle to expose start/end state discontinuities.
    actor['clips'].insert(2, idles[1])
    actor['clips'].insert(0, {**idles[0], 'label': 'idle before pickup'})
    actor['clips'].append({**idles[0], 'label': 'idle after deposit'})
(OUT / 'locker-review.json').write_text(json.dumps({'actors': actors, 'continuousVisualAcceptance': False}, indent=2) + '\n', encoding='utf-8')
print('Locker review: action sources and bare/equipped idle cycles verified for all three crew. Visual join acceptance remains open.')
