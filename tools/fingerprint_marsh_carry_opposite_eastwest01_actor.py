"""Bound actual opposite fixture plus allquarter/half/family source dependencies."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1'
names=['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn']
names+=['tools/'+n for n in ['assemble_marsh_carry_opposite01.py','prepare_marsh_carry_opposite_eastwest01_native.py','review_marsh_carry_opposite_eastwest01_actor.gd','review_marsh_carry_opposite_eastwest01_actor.gd.uid','publish_marsh_carry_opposite_eastwest01_actor.py','fingerprint_marsh_carry_opposite_eastwest01_actor.py','review_marsh_carry_turn_eastsouth01_actor.gd','publish_marsh_carry_turn_eastsouth01_actor.py']]
paths=[ROOT/n for n in names]+list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'));assert all(p.exists() for p in paths)
for folder in ['sources','east-south-01-unselected','west-south-02-unselected','east-north-02-unselected','west-north-01-unselected','opposite-01-unselected']:paths+=[p for p in (B/folder).rglob('*') if p.is_file()]
for f,rev in [('east','03'),('west','03')]:paths+=list((ROOT/f'character/marsh-{f}-carry-material-v1/candidate-{rev}').glob('*'))
g=json.loads((B/'sources/guide-provenance.json').read_text());paths+=[ROOT/r['path'] for k in ['primaryIdles','ownOriginalMasters'] for r in g[k].values()]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()};Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded East-West opposite inputs')
