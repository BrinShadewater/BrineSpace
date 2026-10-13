"""Actual East-to-West reversal through normal actor/player;9turn phases."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/review_marsh_carry_turn_eastsouth01_actor.gd').read_text().replace('carry-turn-east-south-01','carry-opposite-east-west-01').replace('east-south-01-unselected','opposite-01-unselected').replace('south','west').replace('South','West').replace('SOUTH','WEST')
s=s.replace('marsh-west-carry-material-v1/candidate-01/manifest.json','marsh-west-carry-material-v1/candidate-03/manifest.json')
for a,b in [('Vector2(0,96)','Vector2(-96,0)'),('Vector2(64,96)','Vector2(-32,0)'),('Vector2(0,travel)','Vector2(-travel,0)'),('East64/West96','East+64/West-96'),('range(5)','range(9)'),('[4-slot]','[8-slot]'),('player.frames["carry-turn-east-west"][4]','player.frames["carry-turn-east-west"][8]'),('range(140)','range(160)'),('turn_seen.size()==5','turn_seen.size()==9'),('restores==5','restores==9'),(',.4)',',.8)'),('400ms','800ms'),('advance0to4','advance0to8'),('all5turn','all9turn'),('5restores','9restores'),('140controlled','160controlled'),('five moving turn','nine moving turn')]:
    if a=='all5turn':continue # This phrase occurs only in recorder prose,not the fixture.
    assert a in s,a;s=s.replace(a,b)
s=s.replace('staged carries/quarter turn','staged carries/800ms opposite turn')
p=ROOT/'tools/review_marsh_carry_opposite_eastwest01_actor.gd';assert not p.exists();p.write_text(s);p.with_suffix('.gd.uid').write_text('uid://di6ehopp1v02\n')
s=(ROOT/'tools/publish_marsh_carry_turn_eastsouth01_actor.py').read_text().replace('carry-turn-east-south-01','carry-opposite-east-west-01').replace('east-south-01-actor-review','opposite-east-west-01-actor-review').replace('east-south-01-unselected','opposite-01-unselected').replace('south','west')
s=s.replace('marsh-west-carry-material-v1/candidate-01/manifest.json','marsh-west-carry-material-v1/candidate-03/manifest.json')
for a,b in [("r['actorRestores']==5","r['actorRestores']==9"),("len(r['samples'])==140","len(r['samples'])==160"),('list(range(5))','list(range(9))'),('len(captures)==12','len(captures)==16'),("['carry-turn-east-west']*5","['carry-turn-east-west']*9"),('captures[2:7]','captures[2:11]'),('captures[7:11]','captures[11:15]'),('range(3)','range(4)'),('timing=[60,90,100,90,60]','timing=[60,90,100,90,120,90,100,90,60]'),('turn=crops[2:7]','turn=crops[2:11]'),('len(decoded)==5','len(decoded)==9'),('allTwelvePairsInspected','allSixteenPairsInspected'),("'captures':12","'captures':16"),("'exactSources':12","'exactSources':16"),("'controlledSamples':140","'controlledSamples':160"),("'actorPlayerRestores':5","'actorPlayerRestores':9"),('allFiveTurnPhases','allNineTurnPhases'),('Five exact cropped held captures at60/90/100/90/60ms','Nine exact cropped held captures at60/90/100/90/120/90/100/90/60ms')]:
    assert a in s,a;s=s.replace(a,b)
s=s.replace("'retainedFailure':'failed-parse stores initial type-inference failure before startup;corrected declaration only,no artwork change.'","'retainedFailure':'None in this independent opposite interval;explicit bool retained.'")
p=ROOT/'tools/publish_marsh_carry_opposite_eastwest01_actor.py';assert not p.exists();p.write_text(s)
print('Actual East+64/West-96 U-turn fixture+UID/publisher;160samples/9turnphase-restores/16captures expected.')
