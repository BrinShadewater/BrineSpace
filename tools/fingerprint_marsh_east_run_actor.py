"""Bound staged run source/controller inputs, excluding output/doc mutations."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
paths=[ROOT/p for p in ['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn','tools/review_marsh_east_run_actor.gd','tools/review_marsh_east_run_actor.gd.uid','tools/fingerprint_marsh_east_run_actor.py','tools/prepare_marsh_east_run_guides.py','tools/prepare_marsh_east_run_prompt.py','tools/build_marsh_east_run01.py']]
paths+=list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'))
for folder in ['sources','candidate-01']:paths+=list((BASE/folder).glob('*'))
guide=json.loads((BASE/'sources/guide-provenance.json').read_text());paths += [ROOT/r['path'] for r in guide['primarySourceFrames']+guide['guideSourceFrames']]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded staged run inputs')
