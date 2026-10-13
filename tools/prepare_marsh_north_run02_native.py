"""Reverse the physical South fixture interval for own-art North actor review."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
source = (ROOT/'tools/review_marsh_south_run05_actor.gd').read_text().replace('marsh-south-run-material-v1','marsh-north-run-material-v1').replace('south-run-actor-05','north-run-actor-02').replace('candidate-05','candidate-02').replace('run-south','run-north').replace('"south"','"north"').replace('South','North').replace('SOUTH RUN','NORTH RUN')
start = source.index('\tactor.foot=route_start;')
prefix, tail = source[:start], source[start:]
old = 'if clear and actor.segment_clear(candidate,candidate+Vector2(0,168)):route_start=candidate;break'
assert old in prefix
prefix = prefix.replace(old,'if clear and actor.segment_clear(candidate+Vector2(0,168),candidate):route_start=candidate+Vector2(0,168);break')
tail = tail.replace('Vector2(0,168)','Vector2(0,-168)').replace('actor.foot.y>=before.y and actor.foot.y<=route_start.y+168','actor.foot.y<=before.y and actor.foot.y>=route_start.y-168').replace('planted sole plane or airborne clearance in actual loaded texture','whole texture bbox anchor or flight clearance; not anatomical contact proof')
target = ROOT/'tools/review_marsh_north_run02_actor.gd'
assert not target.exists()
target.write_text(prefix+tail)
target.with_suffix('.gd.uid').write_text('uid://cw4nhrunm7v90\n')
publisher = (ROOT/'tools/publish_marsh_west_run02_actor.py').read_text().replace('west','north').replace('West','North').replace('neutral147occupied','neutral146occupied')
(ROOT/'tools/publish_marsh_north_run02_actor.py').write_text(publisher)
print('Prepared actual North movement/render/restore review on reversed clear168world vertical interval.')
