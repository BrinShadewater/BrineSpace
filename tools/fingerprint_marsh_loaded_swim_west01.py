"""Bounded source/reference/fixture interval fingerprint for the native study."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1'
paths=[ROOT/'project.godot',ROOT/'scripts/crew_sprite_player.gd',ROOT/'scripts/crew_sprite_player.gd.uid',ROOT/'character/marsh-v2/catalog.json']
paths += [ROOT/'tools'/n for n in ['prepare_marsh_loaded_swim_material01.py','prepare_marsh_loaded_swim_material02.py','pack_marsh_loaded_swim_material01.py','pack_marsh_loaded_swim_material02.py','prepare_marsh_loaded_swim_native02.py','review_marsh_loaded_swim_west01.gd','review_marsh_loaded_swim_west01.gd.uid','fingerprint_marsh_loaded_swim_material02.py']]
for revision in ['01','02']:
    p=B/f'sources/east-loop-{revision}.request.json';paths.append(p);r=json.loads(p.read_text())
    paths += [B/f'sources/east-loop-{revision}.prompt.txt',B/f'sources/east-loop-{revision}.raw.png']
    paths += [ROOT/q['path'] for q in r['orderedReferences']+r['sourceFrames']]
    paths.append(ROOT/r['selectedMotionManifest']['path'])
    paths += list((B/f'east-loop-{revision}-unselected').glob('*.png'))
    paths.append(B/f'east-loop-{revision}-unselected/recipe.json')
paths.append(B/'east-loop-02-unselected/manifest.json')
paths += [ROOT/'tools'/n for n in ['prepare_marsh_loaded_swim_west01.py','retain_pack_marsh_loaded_swim_west01.py','pack_marsh_loaded_swim_west01.py','prepare_marsh_loaded_swim_west_native01.py','prepare_marsh_loaded_swim_west_native01_generated.py','fingerprint_marsh_loaded_swim_west01.py']]
request=json.loads((B/'sources/west-loop-01.request.json').read_text());paths+=[ROOT/q['path'] for q in request['orderedReferences']+request['sourceFrames']]
paths += [p for p in (B/'sources').glob('west-*') if p.suffix in ['.png','.json','.txt']]
paths += list((B/'west-loop-01-unselected').glob('*'))
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded loaded-swim study inputs')
