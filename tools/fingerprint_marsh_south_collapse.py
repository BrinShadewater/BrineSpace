"""Bounded source/playback fingerprint; not every catalog-loaded artwork."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
base=ROOT/'character/marsh-south-collapse-material-v1'
request=json.loads((base/'sources/collapse-01.request.json').read_text())
paths=[ROOT/p for p in ['project.godot','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','character/marsh-v2/catalog.json','tools/prepare_marsh_south_collapse.py','tools/build_marsh_south_collapse.py','tools/review_marsh_south_collapse.gd','tools/review_marsh_south_collapse.gd.uid','tools/fingerprint_marsh_south_collapse.py']]
paths += [ROOT/item['path'] for item in request['orderedReferences']+request['guideSourceFrames']]
paths += list((base/'sources').glob('*'))+list((base/'candidate-01').glob('*'))
result={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(len(result),'bounded dry-collapse source/playback fingerprints saved')
