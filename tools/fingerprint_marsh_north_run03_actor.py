"""Freeze bounded North sources, whole-pack dependencies and native consumers."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-run-material-v1'
names=['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn']
names+=['tools/'+n for n in ['review_marsh_north_run03_actor.gd','review_marsh_north_run03_actor.gd.uid','prepare_marsh_north_run03_native.py','fingerprint_marsh_north_run03_actor.py','publish_marsh_north_run03_actor.py','prepare_marsh_north_run_guides.py','prepare_marsh_west_run_guides.py','prepare_marsh_north_run01.py','build_marsh_north_run01.py','build_marsh_west_run01.py','prepare_marsh_north_contacts02.py','build_marsh_north_contacts02.py','prepare_marsh_north_passing03.py','build_marsh_north_passing03.py','assemble_marsh_north_run02.py','assemble_marsh_west_run02.py','review_marsh_south_run05_actor.gd','rebuild_bill_art.py','prepare_marsh_north_passing04.py','build_marsh_north_passing04.py','build_marsh_north_passing03.py','assemble_marsh_north_run03.py','review_marsh_north_run02_actor.gd','prepare_marsh_north_run02_native.py']]
paths=[ROOT/n for n in names]+list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'))
for folder in ['sources','candidate-01','candidate-02','contacts-02-unselected','passing-03-unselected','passing-04-unselected','candidate-03']:
    paths+=list((BASE/folder).glob('*'))
guide=json.loads((BASE/'sources/guide-provenance.json').read_text())
paths+=[ROOT/r['path'] for r in guide['primarySourceFrames']+guide['guideSourceFrames']]
for p in (BASE/'sources').glob('*.request.json'):
    paths+=[ROOT/r['path'] for r in json.loads(p.read_text())['orderedReferences']]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()}
Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n')
print(len(data),'bounded North staged inputs')
