"""Select each authored helmet pose once and give contact stages explicit timing.

No PNG edits. Run after a source rebuild; existing palette processing is separate.
The original 12-slot selections are preserved in helmet-transition-polish-v1.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/helmet-transition-polish-v1'
KEYS = {'veld': [0, 1, 2, 4, 6, 8, 10, 11],
        'branforth': [0, 1, 2, 4, 7, 8, 9, 11]}
DURATIONS = {'equip': [140, 260, 300, 280, 300, 340, 280, 240],
             'remove': [140, 300, 340, 320, 300, 300, 300, 240]}


def apply(actor):
    baseline = json.loads((BASE / 'selected.json').read_text())[actor]
    equip = baseline['body/equip-helmet-east']
    for action in ['equip', 'remove']:
        key = action + '-helmet-east'
        record = baseline['body/' + key]
        path = ROOT / record['manifest']
        pack = json.loads(path.read_text())
        state = next(s for s in pack['states'] if s['id'] == key)
        order = KEYS[actor] if action == 'equip' else KEYS[actor][::-1]
        # Both actions share the very same source images, including idle joins.
        source_dir = (ROOT / equip['manifest']).parent
        import os
        state['frameFiles'] = [os.path.relpath(source_dir / equip['state']['frameFiles'][i], path.parent).replace('\\', '/') for i in order]
        state['frameDurationsMs'] = DURATIONS[action]
        for field in ['facings', 'waterKinds', 'waterPoses', 'depthOffsets']:
            original = record['state'][field]
            assert len(set(original)) == 1, field
            state[field] = [original[0]] * len(order)
        assert sum(state['frameDurationsMs']) == sum(record['state']['frameDurationsMs'])
        path.write_text(json.dumps(pack, indent=2) + '\n')


if __name__ == '__main__':
    for actor in KEYS:
        apply(actor)
    print('Updated four clips: eight authored poses, unchanged 2.14s/2.24s action durations; no image edits.')
