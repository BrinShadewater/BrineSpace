"""Straight northern site proves North pickup; airlock rotation alone cannot."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_water_transition_world03.gd').read_text()
s=s.replace('water-transition-world-03','water-transition-world-05').replace('WORLD03','WORLD05')
s=s.replace('Vector2i(21,20);var target:=Vector2i(24,21)','Vector2i(20,19);var target:=Vector2i(20,16)')
s=s.replace('for y in range(20,22):','for y in range(16,20):').replace('for x in range(21,25):','for x in [20,21]:').replace('game.occupied[home].rotation=1','game.occupied[home].rotation=0')
s=s.replace('key=="swim-carry-north"','key=="swim-carry-south"').replace('all six north timing slots','all six south timing slots').replace('dispatched q1','dispatched q0 straight North site').replace('return/north staged loop','return/south staged loop')
needle='if actor.expedition.is_empty():quit(1);return'
s=s.replace(needle,needle+'\n\tvar planned:PackedVector2Array=actor.expedition.sea_route\n\tcheck(planned.size()>=2 and actor.travel_heading(planned[-2],planned[-1],"south")=="north","normal planned final site approach is North")')
s=s.replace('if phase=="pickup":pickup[slot]=true','if phase=="pickup":\n\t\t\tcheck(key=="swim-pickup-north","actual North pickup source required");pickup[slot]=true')
p=ROOT/'tools/review_marsh_water_transition_world05.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://bh4p9mq2nv6k\n')
f=(ROOT/'tools/fingerprint_marsh_water_transition_world03.py').read_text().replace('water_transition_world03','water_transition_world05')
f=f.replace("'prepare_marsh_water_transition_world05.py',","'prepare_marsh_water_transition_world03.py','prepare_marsh_water_transition_world05.py',")
(ROOT/'tools/fingerprint_marsh_water_transition_world05.py').write_text(f)
print('Normal straight North site fixture prepared with actual pickup-heading gate.')
