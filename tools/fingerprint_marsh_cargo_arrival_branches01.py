"""Freeze code, staged families and selected metadata for complete-route interval."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
paths=[ROOT/'project.godot',ROOT/'scenes/main.tscn',ROOT/'character/marsh-v2/catalog.json']
paths+=list((ROOT/'scripts').glob('*.gd'))+list((ROOT/'scripts').glob('*.gd.uid'))
paths+=[ROOT/'tools'/n for n in ['prepare_marsh_cargo_arrival_branches01.py','review_marsh_cargo_arrival_branches01_actor.gd','review_marsh_cargo_arrival_branches01_actor.gd.uid','fingerprint_marsh_cargo_arrival_branches01.py']]
manifests=[ROOT/'character/marsh-cargo-held-material-v1/side02-cross-review/family-manifest.json',ROOT/'character/marsh-carry-turn-material-v1/opposite-01-unselected/family-manifest.json']
for f,rev in [('east','03'),('west','03'),('south','01'),('north','01')]:manifests.append(ROOT/f'character/marsh-{f}-carry-material-v1/candidate-{rev}/manifest.json')
catalog=ROOT/'character/marsh-v2/catalog.json'
for n in json.loads(catalog.read_text())['body']:
    paths.append(ROOT/n.removeprefix('res://') if n.startswith('res://') else (catalog.parent/n).resolve())
for p in manifests:
    paths.append(p)
    for s in json.loads(p.read_text())['states']:
        for n in s['frameFiles']:paths.append(ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve())
for f,rev in [('east','02'),('west','02'),('south','01'),('north','01')]:
    p=ROOT/f'character/marsh-cargo-held-material-v1/sources/{f}-unload-{rev}.request.json';paths.append(p)
    r=json.loads(p.read_text());paths+=[ROOT/q['path'] for q in r['sourceFrames']+r['orderedReferences']]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded complete-delivery inputs')
