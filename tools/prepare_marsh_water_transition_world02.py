"""Normal q2 dispatch uses own West pickup and own South drain."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1';O=B/'combined02-cross-review';O.mkdir(exist_ok=True)
data=json.loads((B/'combined01-cross-review/manifest-list.json').read_text())
data['manifests'] +=['character/marsh-water-transition-material-v1/pickup-west-03-unselected/manifest.json','character/marsh-water-transition-material-v1/drain-south-01-unselected/manifest.json']
(O/'manifest-list.json').write_text(json.dumps(data,indent=2)+'\n')
s=(ROOT/'tools/review_marsh_water_transition_world01.gd').read_text()
for a,b in [('water-transition-world-01','water-transition-world-02'),('Vector2i(20,19);var target:=Vector2i(21,16)','Vector2i(20,21);var target:=Vector2i(19,24)'),('game.occupied[home].rotation=0','game.occupied[home].rotation=2'),('key=="swim-carry-west"','key=="swim-carry-east"'),('all six West timing slots','all six East timing slots'),('dispatched q0','dispatched q2'),('pickupEast02/drainNorth01','pickupEast02/drainNorth01/pickupWest03/drainSouth01'),('MARSH WATER TRANSITION WORLD01','MARSH WATER TRANSITION WORLD02')]:s=s.replace(a,b)
needle='check(game.marsh_npc.get_script()==Normal';assert needle in s
s=s.replace(needle,'player.load_manifest("res://character/marsh-water-transition-material-v1/pickup-west-03-unselected/manifest.json",true)\n\tplayer.load_manifest("res://character/marsh-water-transition-material-v1/drain-south-01-unselected/manifest.json",true)\n\t'+needle)
s=s.replace('for y in range(16,20):','for y in range(21,25):').replace('for x in [20,21]:','for x in [19,20]:')
s=s.replace('water-transition-world-02-2026-10-03/','water-transition-world-02-2026-10-03-retry1/')
s=s.replace('check(Trips.dispatch(game,"marsh",home),"actual normal expedition dispatch")','check(Trips.dispatch(game,"marsh",home),"actual normal expedition dispatch; reason="+Trips.reason(game,"marsh",home))')
p=ROOT/'tools/review_marsh_water_transition_world02.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://dp8mh4vq6nk2\n')
f=(ROOT/'tools/fingerprint_marsh_water_transition_world01.py').read_text().replace('water_transition_world01','water_transition_world02')
(ROOT/'tools/fingerprint_marsh_water_transition_world02.py').write_text(f)
print('Normal q2 Westpickup/Southdrain fixture prepared; original per-manifest pivots retained.')
