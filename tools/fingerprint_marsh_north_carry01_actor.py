"""Bound North carry sources, authored fixture and normal runtime consumers."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-north-carry-material-v1'
names=['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn']
names+=['tools/'+n for n in ['prepare_marsh_north_carry_guides.py','prepare_marsh_north_carry01.py','build_marsh_north_carry01.py','rebuild_bill_art.py','prepare_marsh_north_carry01_native.py','review_marsh_north_carry01_actor.gd','review_marsh_north_carry01_actor.gd.uid','fingerprint_marsh_north_carry01_actor.py','publish_marsh_north_carry01_actor.py','review_marsh_south_run05_actor.gd','publish_marsh_west_run02_actor.py','prepare_marsh_south_carry_guides.py','build_marsh_south_carry01.py','prepare_marsh_south_carry01_native.py','review_marsh_south_carry01_actor.gd','publish_marsh_south_carry01_actor.py']]
paths=[ROOT/n for n in names]+list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'))
for folder in ['sources','candidate-01']:paths+=list((BASE/folder).glob('*'))
g=json.loads((BASE/'sources/guide-provenance.json').read_text());paths+=[ROOT/r['path'] for r in g['primarySourceFrames']+g['guideSourceFrames']+[g['originalOwnMaster']]]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded North cargo inputs')
