"""Bounded selected gesture, source/pack code and native player dependencies."""
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT / 'project.godot', Path(__file__)]
paths += list((ROOT / 'scripts').glob('*.gd')) + list((ROOT / 'scripts').glob('*.gd.uid'))
paths += [ROOT / ('tools/review_marsh_retained_gesture_south03.gd' + suffix) for suffix in ['', '.uid']]
paths += [ROOT / 'tools/prepare_marsh_retained_gesture_south.py', ROOT / 'tools/build_marsh_retained_gesture_south.py']
base = ROOT / 'character/marsh-retained-gesture-material-v1'
paths += list((base / 'sources').glob('*')) + list((base / 'inputs').glob('*.png'))
paths += list((base / 'south03-unselected').glob('*.png'))
manifest = base / 'south03-unselected/manifest.json'
paths.append(manifest)
for state in json.loads(manifest.read_text())['states']:
    paths += [ROOT / p.removeprefix('res://') for p in state['frameFiles']]
paths += [ROOT / f'character/marsh-v2/frames/bare/remove-helmet-south/{i:03}.png' for i in range(6)]
records = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
Path(sys.argv[1]).write_text(json.dumps(records, indent=2) + '\n')
print(len(records), 'bounded retained gesture inputs')
