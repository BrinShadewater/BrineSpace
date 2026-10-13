"""Fingerprint current directed turn, cardinal loop inputs and authorities."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';r=json.loads((B/'sources/east-south-01.request.json').read_text())
paths=[ROOT/'project.godot',ROOT/'scripts/crew_sprite_player.gd',ROOT/'scripts/crew_sprite_player.gd.uid',ROOT/'character/marsh-v2/catalog.json']
paths +=[ROOT/q['path'] for q in r['orderedReferences']+r['sourceFrames']]+[ROOT/r['selectedTurnManifest']['path']]
paths +=list((B/'sources').glob('east-south-01.*'))+list((B/'east-south-01-unselected').glob('*'))
paths +=[ROOT/'tools/pack_marsh_loaded_swim_turn_south01.py',ROOT/'tools/prepare_marsh_loaded_swim_turn_south_native01.py']
paths +=list((ROOT/'tools').glob('*marsh_loaded_swim_turn_eastsouth*'))
cardinal=ROOT/'character/marsh-loaded-swim-material-v1/cardinal01-cross-review/family-manifest.json';paths.append(cardinal)
for state in json.loads(cardinal.read_text())['states']:
    paths +=[ROOT/n.removeprefix('res://') for n in state['frameFiles']]
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded turn/cardinal inputs')
