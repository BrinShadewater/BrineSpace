"""Freeze normal code, selected metadata and staged East action source for interval."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
paths=[ROOT/'project.godot',ROOT/'scenes/main.tscn',ROOT/'character/marsh-v2/catalog.json']
paths += list((ROOT/'scripts').glob('*.gd'))+list((ROOT/'scripts').glob('*.gd.uid'))
paths += [ROOT/'tools'/n for n in ['prepare_marsh_cargo_side_action02.py','review_marsh_cargo_side_action02_actor.gd','review_marsh_cargo_side_action02_actor.gd.uid','fingerprint_marsh_cargo_side_action02.py','pack_marsh_cargo_east_unload02.py','pack_marsh_cargo_west_unload02.py','prepare_marsh_cargo_side_packers02.py']]
for folder in ['character/marsh-cargo-held-material-v1/sources','character/marsh-cargo-held-material-v1/east-unload-02-unselected','character/marsh-cargo-held-material-v1/west-unload-02-unselected','character/marsh-east-carry-material-v1/candidate-03','character/marsh-west-carry-material-v1/candidate-03','character/marsh-south-carry-material-v1/candidate-01']:
    paths += [p for p in (ROOT/folder).rglob('*') if p.is_file()]
catalog=ROOT/'character/marsh-v2/catalog.json'
for n in json.loads(catalog.read_text())['body']:
    p=ROOT/n.removeprefix('res://') if n.startswith('res://') else (catalog.parent/n).resolve();paths.append(p)
for n in ['character/marsh-v2/frames/bare/idle-east/000.png']:
    paths.append(ROOT/n)
for f in ['east','west']:
    request=json.loads((ROOT/f'character/marsh-cargo-held-material-v1/sources/{f}-unload-02.request.json').read_text())
    paths += [ROOT/q['path'] for q in request['sourceFrames']+request['orderedReferences']]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded cargo action inputs')
