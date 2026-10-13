"""Adapt known actual path-corner fixture for independent negative-X West leg."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_carry_turn_eastsouth01_actor.gd').read_text()
s=s.replace('east-south-01','west-south-02').replace('eastsouth01','westsouth02').replace('marsh-east-carry','marsh-west-carry').replace('east','west').replace('East','West').replace('EAST','WEST')
assert 'Vector2(64,0)' in s and 'Vector2(64,96)' in s and 'Vector2(travel,0)' in s
s=s.replace('Vector2(64,0)','Vector2(-64,0)').replace('Vector2(64,96)','Vector2(-64,96)').replace('Vector2(travel,0)','Vector2(-travel,0)').replace('West64/South96','West-64/South96')
p=ROOT/'tools/review_marsh_carry_turn_westsouth02_actor.gd';assert not p.exists();p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://df3whstrn2v99\n')
publisher=(ROOT/'tools/publish_marsh_carry_turn_eastsouth01_actor.py').read_text().replace('east-south-01','west-south-02').replace('marsh-east-carry','marsh-west-carry').replace('idle-east','idle-west').replace('carry-east','carry-west').replace('carry-turn-east-south','carry-turn-west-south')
publisher=publisher.replace("'retainedFailure':'failed-parse stores initial type-inference failure before startup;corrected declaration only,no artwork change.'","'retainedFailure':'None in this independent West native interval;East fixture explicit bool retained.'")
q=ROOT/'tools/publish_marsh_carry_turn_westsouth02_actor.py';assert not q.exists();q.write_text(publisher)
print('Independent actual West negativeX64/South96 fixture+UID/publisher prepared;normal runtime unchanged.')
