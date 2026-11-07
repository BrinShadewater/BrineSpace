"""Bounded East whole-source and actual native actor interval."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-collapse-material-v1'
paths=[ROOT/p for p in ['project.godot','scripts/main.gd','scenes/main.tscn','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/marsh_npc.gd','scripts/marsh_south_snapshot.gd','scripts/marsh_ground_motion.gd','scripts/marsh_west_motion.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','rooms/whole-room/nursery_whole_view.gd','character/marsh-v2/catalog.json','tools/prepare_marsh_east_damage_guides.py','tools/prepare_marsh_east_collapse_prompt.py','tools/retain_marsh_east_collapse_source.py','tools/prepare_marsh_east_collapse_builder.py','tools/build_marsh_east_collapse.py','tools/prepare_marsh_east_collapse_fixture.py','tools/review_marsh_east_collapse_actor.gd','tools/review_marsh_east_collapse_actor.gd.uid','tools/fingerprint_marsh_east_collapse.py']]
for directory in ['sources','candidate-01']:paths+=list((BASE/directory).glob('*'))
req=json.loads((BASE/'sources/collapse-01.request.json').read_text())
paths+=[ROOT/r['path'] for r in req['orderedReferences']+req['primarySourceFrames']+req['guideSourceFrames']]
records={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(records,indent=2)+'\n');print(len(records),'bounded East collapse inputs saved')
