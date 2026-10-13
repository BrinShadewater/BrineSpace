"""Create assembly tool and actual positiveX-to-negativeY quarter-turn fixture."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
assembly=(ROOT/'tools/assemble_marsh_carry_turn_westsouth02.py').read_text()
assembly=assembly.replace('west-south','east-north').replace('south-west','north-east').replace('west-south-nearfront05','east-north-nearback03').replace('east-north-nearfront05','east-north-nearback03').replace('nearfront05','nearback03').replace('selectedSouth','selectedNorth')
assembly=assembly.replace('Nearfront05 left head and frontal body checked provisionally;full grade/head/case/foot joins remain for consistency polish.','Nearback03 rear-right head/body and viewerLEFT support checked provisionally;first intermediate remains close to East side and full grade/head/case/foot joins need consistency polish.')
p=ROOT/'tools/assemble_marsh_carry_turn_eastnorth02.py';assert not p.exists();p.write_text(assembly)
s=(ROOT/'tools/review_marsh_carry_turn_eastsouth01_actor.gd').read_text().replace('east-south-01','east-north-02').replace('south','north').replace('South','North').replace('SOUTH','NORTH')
for a,b in [('Vector2(0,96)','Vector2(0,-96)'),('Vector2(64,96)','Vector2(64,-96)'),('Vector2(0,travel)','Vector2(0,-travel)'),('East64/North96','East64/North-96')]:
    assert a in s;s=s.replace(a,b)
p=ROOT/'tools/review_marsh_carry_turn_eastnorth02_actor.gd';assert not p.exists();p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://dg4ehstrn2v00\n')
s=(ROOT/'tools/publish_marsh_carry_turn_eastsouth01_actor.py').read_text().replace('east-south-01','east-north-02').replace('south','north')
s=s.replace("'retainedFailure':'failed-parse stores initial type-inference failure before startup;corrected declaration only,no artwork change.'","'retainedFailure':'None in this independent East-North interval;explicit bool from earlier fixture retained.'")
p=ROOT/'tools/publish_marsh_carry_turn_eastnorth02_actor.py';assert not p.exists();p.write_text(s)
print('Created whole replacement assembly and independent East64/North-96 native fixture+UID/publisher.')
