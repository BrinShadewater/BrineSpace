"""Independent actual negativeX-to-negativeY West/North quarter fixture."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_carry_turn_westsouth02_actor.gd').read_text().replace('west-south-02','west-north-01').replace('south','north').replace('South','North').replace('SOUTH','NORTH')
for a,b in [('Vector2(0,96)','Vector2(0,-96)'),('Vector2(-64,96)','Vector2(-64,-96)'),('Vector2(0,travel)','Vector2(0,-travel)'),('West-64/North96','West-64/North-96')]:
    assert a in s;s=s.replace(a,b)
p=ROOT/'tools/review_marsh_carry_turn_westnorth01_actor.gd';assert not p.exists();p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://dh5whstrn1v01\n')
s=(ROOT/'tools/publish_marsh_carry_turn_westsouth02_actor.py').read_text().replace('west-south-02','west-north-01').replace('south','north').replace('West native interval','West-North native interval')
p=ROOT/'tools/publish_marsh_carry_turn_westnorth01_actor.py';assert not p.exists();p.write_text(s)
print('Independent actual WestnegativeX64/NorthnegativeY96 fixture+UID/publisher prepared.')
