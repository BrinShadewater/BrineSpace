"""Bound own West-North turn,normal actor/player and actual fixture."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-carry-turn-material-v1'
names=['project.godot','character/marsh-v2/catalog.json','scripts/main.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','scripts/bill_npc.gd','scripts/loading_transition.gd','scripts/title_settings.gd','scripts/room_layout_store.gd','scenes/main.tscn']
names+=['tools/'+n for n in ['prepare_marsh_carry_turn_material_guides.py','prepare_marsh_carry_turn_westnorth01.py','build_marsh_carry_turn_material.py','rebuild_bill_art.py','prepare_marsh_carry_turn_westnorth01_native.py','review_marsh_carry_turn_westnorth01_actor.gd','review_marsh_carry_turn_westnorth01_actor.gd.uid','fingerprint_marsh_carry_turn_westnorth01_actor.py','publish_marsh_carry_turn_westnorth01_actor.py','review_marsh_carry_turn_westsouth02_actor.gd','publish_marsh_carry_turn_westsouth02_actor.py']]
paths=[ROOT/n for n in names]+list((ROOT/'scripts').glob('marsh*.gd'))+list((ROOT/'scripts').glob('marsh*.gd.uid'));assert all(p.exists() for p in paths)
for folder in ['sources','west-north-01-unselected']:paths+=[p for p in (B/folder).rglob('*') if p.is_file()]
for f,rev in [('west','03'),('north','01')]:paths+=list((ROOT/f'character/marsh-{f}-carry-material-v1/candidate-{rev}').glob('*'))
g=json.loads((B/'sources/guide-provenance.json').read_text());paths+=[ROOT/r['path'] for k in ['primaryIdles','ownOriginalMasters'] for r in g[k].values()]
data={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file()};Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n');print(len(data),'bounded West-North turn inputs')
