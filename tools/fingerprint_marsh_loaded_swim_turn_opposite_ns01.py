"""Bounded combined source/manifest/player stability around the opposite study."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1'
r=json.loads((B/'sources/opposite-ns-01.request.json').read_text())
paths=[ROOT/'project.godot',ROOT/'scripts/crew_sprite_player.gd',ROOT/'scripts/crew_sprite_player.gd.uid']+[ROOT/q['path'] for q in r['orderedInputs']]
paths +=[B/'sources/opposite-ns-01.request.json']+list((B/'opposite-ns-01-unselected').glob('*'))+list((ROOT/'tools').glob('*marsh_loaded_swim_turn_opposite_ns*'))
for stem in ['east-north-02','east-south-01','west-south-01']:
    request=B/f'sources/{stem}.request.json';q=json.loads(request.read_text());paths +=[request,B/f'sources/{stem}.prompt.txt',B/f'sources/{stem}.raw.png']+[ROOT/n['path'] for n in q['orderedReferences']+q['sourceFrames']]
    paths +=list((B/f'{stem}-unselected').glob('*.png'))+[B/f'{stem}-unselected/recipe.json']
family=ROOT/'character/marsh-loaded-swim-material-v1/cardinal01-cross-review/family-manifest.json'
for state in json.loads(family.read_text())['states']:paths +=[ROOT/n.removeprefix('res://') for n in state['frameFiles']]
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded composed opposite inputs')
