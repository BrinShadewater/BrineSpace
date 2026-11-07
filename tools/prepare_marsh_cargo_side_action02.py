"""Normal timed-state playback for whole East/West02 redraws."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_cargo_southwest_action01_actor.gd').read_text()
s=s.replace('cargo-southwest-action-01-2026-10-02','cargo-side-action-02-2026-10-02')
s=s.replace('south-unload-01-unselected','east-unload-02-unselected').replace('west-unload-01-unselected','west-unload-02-unselected')
s=s.replace('[["south","pickup"],["south","unload"],["west","pickup"],["west","unload"]]','[["east","pickup"],["east","unload"],["west","pickup"],["west","unload"]]')
s=s.replace('South andWest','East andWest').replace('MARSH SOUTHWEST ACTION','MARSH SIDE02 ACTION')
(ROOT/'tools/review_marsh_cargo_side_action02_actor.gd').write_text(s)
(ROOT/'tools/review_marsh_cargo_side_action02_actor.gd.uid').write_text('uid://dq4cargoact2v08\n')
finger=(ROOT/'tools/fingerprint_marsh_cargo_southwest_action01.py').read_text().replace('cargo_southwest_action01','cargo_side_action02')
finger=finger.replace('pack_marsh_cargo_south_unload01.py','pack_marsh_cargo_east_unload02.py').replace('pack_marsh_cargo_west_unload01.py','pack_marsh_cargo_west_unload02.py').replace('prepare_marsh_cargo_southwest_packers01.py','prepare_marsh_cargo_side_packers02.py')
finger=finger.replace('south-unload-01-unselected','east-unload-02-unselected').replace('west-unload-01-unselected','west-unload-02-unselected')
anchor="data={p.relative_to(ROOT).as_posix()"
assert anchor in finger
finger=finger.replace(anchor,"for f in ['east','west']:\n    request=json.loads((ROOT/f'character/marsh-cargo-held-material-v1/sources/{f}-unload-02.request.json').read_text())\n    paths += [ROOT/q['path'] for q in request['sourceFrames']+request['orderedReferences']]\n"+anchor)
(ROOT/'tools/fingerprint_marsh_cargo_side_action02.py').write_text(finger)
pub=(ROOT/'tools/publish_marsh_cargo_southwest_action01.py').read_text().replace('cargo-southwest-action-01','cargo-side-action-02').replace('southwest-action-01-actor-review','side-action-02-actor-review')
pub=pub.replace("[('south','pickup'),('south','unload'),('west','pickup'),('west','unload')]","[('east','pickup'),('east','unload'),('west','pickup'),('west','unload')]")
pub=pub.replace("for f in ['south','west']","for f in ['east','west']").replace("f'{f}-unload-01-unselected/manifest.json'","f'{f}-unload-02-unselected/manifest.json'")
pub=pub.replace('South/West','East/West')
(ROOT/'tools/publish_marsh_cargo_side_action02.py').write_text(pub)
print('East/West02 timed fixture and exact-source publisher prepared')
