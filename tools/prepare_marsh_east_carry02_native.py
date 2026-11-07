"""Stage East cargo on its validated positive-X furnished route."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
east=(ROOT/'tools/review_marsh_east_run03_actor.gd').read_text();south=(ROOT/'tools/review_marsh_south_carry01_actor.gd').read_text()
prefix=east[:east.index('\tvar old_stride:')].replace('east-run-actor-03','east-carry-actor-02').replace('marsh-east-run-material-v1/candidate-03','marsh-east-carry-material-v1/candidate-02')
tail=south[south.index('\tvar old_stride:'):].replace('south','east').replace('South','East').replace('SOUTH','EAST').replace('Vector2(0,168)','Vector2(168,0)').replace('actor.foot.x==route_start.x','actor.foot.y==route_start.y').replace('actor.foot.y>before.y and actor.foot.y<=route_start.y+168','actor.foot.x>before.x and actor.foot.x<=route_start.x+168')
p=ROOT/'tools/review_marsh_east_carry02_actor.gd';assert not p.exists();p.write_text(prefix+tail);p.with_suffix('.gd.uid').write_text('uid://db9ehcarry2v95\n')
publisher=(ROOT/'tools/publish_marsh_south_carry01_actor.py').read_text().replace('south','east').replace('South','East').replace('carry01','carry02').replace('carry-actor-01','carry-actor-02').replace('candidate-01','candidate-02')
(ROOT/'tools/publish_marsh_east_carry02_actor.py').write_text(publisher)
print('Prepared actual East workshop-carry fixture, paired UID and six-view publisher; unselected.')
