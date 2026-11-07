"""Bound East cargo source sheets, assembled whole cycle and runtime consumers."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-carry-material-v1'
names=['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn']
names+=['tools/'+n for n in ['prepare_marsh_east_carry_guides.py','prepare_marsh_south_carry_guides.py','prepare_marsh_east_carry_contact04.py','prepare_marsh_east_carry_passing05.py','prepare_marsh_east_carry_near06.py','build_marsh_east_carry_contact03.py','build_marsh_east_carry_contact04.py','build_marsh_east_carry_passing05.py','build_marsh_east_carry_half02.py','build_marsh_east_carry_near06.py','build_marsh_north_passing03.py','rebuild_bill_art.py','assemble_marsh_east_carry02.py','prepare_marsh_east_carry02_native.py','review_marsh_east_carry02_actor.gd','review_marsh_east_carry02_actor.gd.uid','fingerprint_marsh_east_carry02_actor.py','publish_marsh_east_carry02_actor.py','review_marsh_east_run03_actor.gd','review_marsh_south_carry01_actor.gd','publish_marsh_south_carry01_actor.py']]
paths=[ROOT/n for n in names]+list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'))
assert all(p.exists() for p in paths),'missing bounded dependency'
for folder in ['sources','candidate-02','contact-04-unselected','passing-05-unselected','near-06-unselected']:paths+=list((BASE/folder).glob('*'))
g=json.loads((BASE/'sources/guide-provenance.json').read_text());paths+=[ROOT/r['path'] for r in g['primarySourceFrames']+g['guideSourceFrames']+[g['originalOwnMaster']]]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded East cargo inputs')

