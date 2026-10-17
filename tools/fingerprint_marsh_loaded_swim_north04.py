"""Fingerprint only the source, authorities, player and this fixture."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1'
r=json.loads((B/'sources/north-loop-04.request.json').read_text())
paths=[ROOT/p for p in ['project.godot','scripts/crew_sprite_player.gd','scripts/crew_sprite_player.gd.uid','character/marsh-v2/catalog.json']]
paths += [ROOT/q['path'] for q in r['orderedReferences']+r['sourceFrames']]+[ROOT/r['selectedMotionManifest']['path']]
paths += list((B/'sources').glob('north-loop-04.*'))+list((B/'north-loop-04-unselected').glob('*'))
paths += list((ROOT/'tools').glob('*marsh_loaded_swim_north*'))
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded inputs')
