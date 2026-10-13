"""Bound West source/controller/route consumers, independent of milestone docs."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-west-run-material-v1'
names=['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn']
names+=['tools/'+p for p in ['review_marsh_west_run02_actor.gd','review_marsh_west_run02_actor.gd.uid','prepare_marsh_west_run02_native.py','fingerprint_marsh_west_run02_actor.py','publish_marsh_west_run02_actor.py','prepare_marsh_west_run_guides.py','prepare_marsh_west_run01.py','build_marsh_west_run01.py','extract_marsh_west_near_half01.py','prepare_marsh_west_half02.py','build_marsh_west_half02.py','assemble_marsh_west_run02.py']]
paths=[ROOT/n for n in names]+list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'))
for folder in ['sources','candidate-02','near-half-01-unselected','far-half-02-unselected']:paths+=list((BASE/folder).glob('*'))
guide=json.loads((BASE/'sources/guide-provenance.json').read_text());paths+=[ROOT/r['path'] for r in guide['primarySourceFrames']+guide['guideSourceFrames']]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()};Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded staged West source/controller inputs')
