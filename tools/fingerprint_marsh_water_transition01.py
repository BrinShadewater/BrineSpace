"""Bounded source/packing/player stability for a transition review."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];mode,side,revision,out=sys.argv[1:5];stem=f'{mode}-{side}-{revision}';B=ROOT/'character/marsh-water-transition-material-v1'
r=json.loads((B/f'sources/{stem}.request.json').read_text())
paths=[ROOT/'project.godot',ROOT/'scripts/crew_sprite_player.gd',ROOT/'scripts/crew_sprite_player.gd.uid',ROOT/'scripts/grid_canvas.gd',ROOT/'scripts/grid_canvas.gd.uid',ROOT/'character/marsh-v2/catalog.json']
paths +=[ROOT/q['path'] for q in r['orderedReferences']+r['sourceFrames']]+[ROOT/r['selectedTransitionManifest']['path']]
paths +=list((B/'sources').glob(stem+'.*'))+list((B/(stem+'-unselected')).glob('*'))
paths +=[ROOT/'tools'/n for n in ['prepare_marsh_water_transition01.py','pack_marsh_water_transition01.py','prepare_marsh_water_pickup_east02.py','prepare_marsh_water_pickup_west02.py','prepare_marsh_water_pickup_west03.py','prepare_marsh_water_pickup_north02.py','prepare_marsh_water_pickup_south02.py','prepare_marsh_water_drain_south02.py','prepare_marsh_water_drain_south03.py','prepare_marsh_water_drain_south04.py','prepare_marsh_water_drain_south05.py','prepare_marsh_water_transition_native01.py','fingerprint_marsh_water_transition01.py',f'review_marsh_water_{mode}_{side}{revision}.gd',f'review_marsh_water_{mode}_{side}{revision}.gd.uid']]
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(out).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded transition inputs')
