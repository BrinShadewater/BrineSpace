"""Freeze current seated source selection and relevant native contact code."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT / p for p in ['project.godot', 'scenes/main.tscn',
                            'character/marsh-v2/catalog.json',
                            'tools/fingerprint_marsh_seated_contact.py']]
paths += list((ROOT / 'scripts').glob('*.gd')) + list((ROOT / 'scripts').glob('*.gd.uid'))
paths += list((ROOT / 'rooms/whole-room').glob('*.gd')) + list((ROOT / 'rooms/whole-room').glob('*.gd.uid'))
for name in ['playtest_marsh_seated_rooms']:
    paths += [ROOT / 'tests' / (name + '.gd'), ROOT / 'tests' / (name + '.gd.uid')]
inventory = json.loads((ROOT / 'character/marsh-full-family-audit-2026-10-03/inventory.json').read_text())
for key, state in inventory['states'].items():
    if key.startswith(('sit-down-', 'sit-idle-', 'sit-rise-', 'read-seated-')):
        paths.append(ROOT / state['manifest'])
        paths += [ROOT / frame['path'] for frame in state['frames']]
data = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data, indent=2) + '\n')
print(len(data), 'bounded seated source/contact inputs')
