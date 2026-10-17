"""Bounded cardinal retained gesture source/native player dependency fingerprint."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-retained-gesture-material-v1'
paths=[ROOT/'project.godot',Path(__file__)]
paths+=list((ROOT/'scripts').glob('*.gd'))+list((ROOT/'scripts').glob('*.gd.uid'))
paths+=[ROOT/('tools/review_marsh_retained_gesture_return06.gd'+suffix) for suffix in ['', '.uid']]
paths+=[ROOT/'tools/prepare_marsh_retained_gesture_cardinal.py',ROOT/'tools/build_marsh_retained_gesture_cardinal.py']
paths += [ROOT/'tools/prepare_marsh_retained_gesture_east04.py',ROOT/'tools/prepare_marsh_retained_gesture_motion_review.py']
paths += [ROOT/'tools/build_marsh_retained_gesture_return06.py']
paths+=list((BASE/'sources').glob('*'))+list((BASE/'inputs').glob('*.png'))
for folder in ['east04-unselected','east05-unselected','east06-unselected','east-return06-unselected','west03-unselected','north02-unselected','south03-unselected','cardinal03-unselected']:
    manifest=BASE/folder/'manifest.json';paths.append(manifest)
    for state in json.loads(manifest.read_text())['states']:
        paths+=[ROOT/p.removeprefix('res://') for p in state['frameFiles']]
old=ROOT/'character/marsh-v2/packs/bare-184x184-p92.0-172.0/manifest.json';paths.append(old)
# Native comparison loads the whole old player bank; freeze all its actual sources.
for state in json.loads(old.read_text())['states']:
    paths+=[ROOT/p.removeprefix('res://') if p.startswith('res://') else (old.parent/p).resolve() for p in state['frameFiles']]
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n')
print(len(records),'bounded cardinal source/player inputs')
