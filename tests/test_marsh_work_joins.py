"""Actual selected cargo/work boundary continuity, separate from historical exports."""
from pathlib import Path
import json
import unittest
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def selected():
    catalog = ROOT / 'character/marsh-v2/catalog.json'
    result = {}
    for relative in json.loads(catalog.read_text())['body']:
        p = (catalog.parent / relative).resolve()
        m = json.loads(p.read_text())
        for state in m['states']:
            result[state['id']] = (p, m, state)
    return result


def registered(record, slot):
    p, m, s = record
    path = s['frameFiles'][slot]
    path = ROOT / path[6:] if path.startswith('res://') else p.parent / path
    image = Image.open(path).convert('RGBA')
    canvas = Image.new('RGBA', (512, 512))
    canvas.paste(image, (256-round(m['pivot'][0]), 256-round(m['pivot'][1])))
    return canvas.tobytes()


class WorkJoins(unittest.TestCase):
    def test_current_whole_body_handoffs(self):
        current = selected()
        for direction in ['east', 'west', 'north', 'south']:
            def pose(action, slot): return registered(current[action+'-'+direction], slot)
            for action, slot in [('pickup', 0), ('unload', -1), ('cargo-unload', -1), ('torch-draw', 0), ('torch-stow', -1)]:
                with self.subTest(direction=direction, action=action):
                    self.assertEqual(pose(action, slot), pose('idle', 0))
            self.assertEqual(pose('torch-draw', -1), pose('weld', 0))
            self.assertEqual(pose('weld', -1), pose('torch-stow', 0))
            for i in range(6):
                self.assertEqual(pose('torch-draw', i), pose('torch-stow', 5-i))

    def test_scoped_contract_and_sources(self):
        import hashlib
        current = selected()
        before = json.loads((ROOT / 'character/marsh-work-review-2026-10-14/selected-before.json').read_text())
        changes = []
        for key, record in before.items():
            p, m, state = current[key]
            self.assertEqual({k:v for k,v in state.items() if k!='frameFiles'}, {k:v for k,v in record['state'].items() if k!='frameFiles'})
            self.assertEqual({k:v for k,v in m.items() if k not in ['states','revision']}, {k:v for k,v in record['metadata'].items() if k!='revision'})
            for slot, old in enumerate(record['files']):
                self.assertEqual(hashlib.sha256((ROOT / old['path']).read_bytes()).hexdigest(), old['sha256'])
                f = state['frameFiles'][slot]
                fp = ROOT / f[6:] if f.startswith('res://') else p.parent / f
                if hashlib.sha256(fp.read_bytes()).hexdigest() != old['sha256']:
                    changes.append((key, slot))
        self.assertEqual(changes, [('torch-draw-south',0),('torch-stow-south',5)])


if __name__ == '__main__': unittest.main()
