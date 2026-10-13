"""Stage own West cargo on the physically reversed validated clear route."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
west=(ROOT/'tools/review_marsh_west_run02_actor.gd').read_text();east=(ROOT/'tools/review_marsh_east_carry03_actor.gd').read_text()
prefix=west[:west.index('\tvar old_stride:')].replace('west-run-actor-02','west-carry-actor-03').replace('marsh-west-run-material-v1/candidate-02','marsh-west-carry-material-v1/candidate-03')
tail=east[east.index('\tvar old_stride:'):].replace('east','west').replace('East','West').replace('EAST','WEST').replace('Vector2(168,0)','Vector2(-168,0)').replace('actor.foot.x>before.x and actor.foot.x<=route_start.x+168','actor.foot.x<before.x and actor.foot.x>=route_start.x-168')
p=ROOT/'tools/review_marsh_west_carry03_actor.gd';assert not p.exists();p.write_text(prefix+tail);p.with_suffix('.gd.uid').write_text('uid://dd1whcarry3v97\n')
publisher=(ROOT/'tools/publish_marsh_east_carry03_actor.py').read_text().replace('east','west').replace('East','West').replace("review=BASE/'actor-review-v2'","review=BASE/'actor-review-v1'")
(ROOT/'tools/publish_marsh_west_carry03_actor.py').write_text(publisher)
print('Prepared actual West workshop-carry fixture/six-pair publisher/UID; own art,negativeX route only.')
