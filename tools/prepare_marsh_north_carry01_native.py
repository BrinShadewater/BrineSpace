"""Reverse physical cargo route while preserving own rear artwork/occlusion."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/review_marsh_south_carry01_actor.gd').read_text().replace('south-carry-actor-01','north-carry-actor-01').replace('marsh-south-carry-material-v1','marsh-north-carry-material-v1').replace('carry-south','carry-north').replace('"south"','"north"').replace('South','North').replace('SOUTH CARRY','NORTH CARRY')
start=source.index('\tactor.foot=route_start;');prefix,tail=source[:start],source[start:]
old='if clear and actor.segment_clear(candidate,candidate+Vector2(0,168)):route_start=candidate;break';assert old in prefix
prefix=prefix.replace(old,'if clear and actor.segment_clear(candidate+Vector2(0,168),candidate):route_start=candidate+Vector2(0,168);break')
tail=tail.replace('route_start+Vector2(0,168)','route_start+Vector2(0,-168)').replace('actor.foot.y>before.y and actor.foot.y<=route_start.y+168','actor.foot.y<before.y and actor.foot.y>=route_start.y-168')
p=ROOT/'tools/review_marsh_north_carry01_actor.gd';assert not p.exists();p.write_text(prefix+tail);p.with_suffix('.gd.uid').write_text('uid://da8nhcarry1v94\n')
publisher=(ROOT/'tools/publish_marsh_south_carry01_actor.py').read_text().replace('south','north').replace('South','North').replace('neutral147occupied','neutral146occupied')
(ROOT/'tools/publish_marsh_north_carry01_actor.py').write_text(publisher)
fingerprint=(ROOT/'tools/fingerprint_marsh_south_carry01_actor.py').read_text().replace('south','north').replace('South','North')
fingerprint=fingerprint.replace("'review_marsh_north_run05_actor.gd'","'review_marsh_south_run05_actor.gd'")
fingerprint=fingerprint.replace("'publish_marsh_west_run02_actor.py']","'publish_marsh_west_run02_actor.py','prepare_marsh_south_carry_guides.py','build_marsh_south_carry01.py','prepare_marsh_south_carry01_native.py','review_marsh_south_carry01_actor.gd','publish_marsh_south_carry01_actor.py']")
(ROOT/'tools/fingerprint_marsh_north_carry01_actor.py').write_text(fingerprint)
print('Prepared actual North workshop cargo fixture on reversed validated vertical route; paired UID and rear-only art.')
