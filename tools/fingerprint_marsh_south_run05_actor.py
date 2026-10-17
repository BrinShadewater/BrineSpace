"""Bound staged run source/controller inputs, excluding output/doc mutations."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
paths=[ROOT/p for p in ['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn','tools/review_marsh_south_run05_actor.gd','tools/review_marsh_south_run05_actor.gd.uid','tools/fingerprint_marsh_south_run05_actor.py','tools/assemble_marsh_south_run04.py','tools/build_marsh_south_run05.py','tools/build_marsh_south_run_passing08.py']]
paths+=list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'))
for folder in ['sources','candidate-03','candidate-04','candidate-05','passing-05-unselected','passing-06-unselected','passing-07-unselected','passing-08-unselected']:paths+=list((BASE/folder).glob('*'))
guide=json.loads((BASE/'sources/guide-provenance.json').read_text());paths += [ROOT/r['path'] for r in guide['primarySourceFrames']+guide['guideSourceFrames']]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded staged run inputs')
