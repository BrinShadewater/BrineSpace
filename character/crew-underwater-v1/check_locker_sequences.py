"""Verify runtime composition provenance and handoff timing without regeneration."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent
expected = {f'{actor}-{action}-east' for actor in ['bill', 'veld', 'branforth']
            for action in ['equip-helmet', 'remove-helmet']}
paths = sorted((ROOT / 'locker').glob('*/manifest.json'))
assert {path.parent.name for path in paths} == expected, 'Missing or unexpected locker sequence'
for path in paths:
    data = json.loads(path.read_text(encoding='utf-8'))
    state = data['states'][0]
    files, durations = state['frameFiles'], state['frameDurationsMs']
    assert len(files) == len(durations) == state['frameCount'] == len(data['sources']) == 12
    assert state['loop'] is False and all(isinstance(d, int) and d > 0 for d in durations)
    assert data['pivot'] == [46, 98]
    for file, source in zip(files, data['sources']):
        resolved = (path.parent / file).resolve()
        assert resolved.is_relative_to(ROOT)
        assert resolved == (ROOT / source['source']).resolve()
        assert hashlib.sha256(resolved.read_bytes()).hexdigest() == source['sha256'], resolved
        with Image.open(resolved) as image:
            assert image.size == (data['frameWidth'], data['frameHeight']) == (92, 104)
            assert image.mode == 'RGBA' and image.getbbox() is not None
    assert data['sources'][5]['sha256'] == data['sources'][6]['sha256']
    join = data['joinTiming']
    assert join['frames'] == [5, 6] and join['composedDurationsMs'] == durations[5:7]
    event_id = 'take-helmet-from-locker' if state['id'].startswith('equip-') else 'release-helmet-to-locker'
    matching = [event for event in state['events'] if event['id'] == event_id]
    assert len(matching) == 1
    for event in state['events']:
        assert 0 <= event['frame'] < len(files)
        assert event['timeMs'] == sum(durations[:event['frame']])
    print(f'{path.parent.name}: source hashes, frame registration and handoff timing PASS')
print('Six runtime sequences verified. This check does not establish visual acceptance.')
