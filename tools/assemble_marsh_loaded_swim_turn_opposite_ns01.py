"""Compose North/South through exact shared East; freeze complete private coverage."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'tools/assemble_marsh_loaded_swim_turn_opposite_ew01.py').read_text()
for a,b in [('opposite-ew','opposite-ns'),('west-north-01-unselected/manifest.json','east-south-01-unselected/manifest.json'),("quarters['swim-carry-turn-east-north']","quarters['swim-carry-turn-north-east']"),("quarters['swim-carry-turn-north-west']","quarters['swim-carry-turn-east-south']"),('east-west','north-south'),('west-east','south-north'),('exact East','exact North'),('EastNorth1','NorthEast1'),('EastNorth2','NorthEast2'),('EastNorth3','NorthEast3'),('exact North /120ms','exact East /120ms'),('NorthWest1','EastSouth1'),('NorthWest2','EastSouth2'),('NorthWest3','EastSouth3'),('exact West','exact South'),('Exact staged North04','Exact staged East02'),('sharedNorth','sharedEast'),('EastNorth02 quarter plus unchanged whole NorthWest01 quarter','NorthEast02 quarter plus unchanged whole EastSouth01 quarter'),('WestEast','SouthNorth'),('EastWest','NorthSouth')]:s=s.replace(a,b)
exec(compile(s,str(__file__),'exec'))
B=ROOT/'character/marsh-loaded-swim-turn-material-v1';O=B/'opposite-ns-01-unselected'
old=json.loads((B/'opposite-ew-01-unselected/family-manifest.json').read_text())
for p in [B/'east-south-01-unselected/manifest.json',B/'west-south-01-unselected/manifest.json',O/'manifest.json']:old['states']+=json.loads(p.read_text())['states']
old['revision']='marsh-loaded-swim-all-turns-family01-staged';old['normalAdmission']=False
assert len(old['states'])==16 and sum(len(q['frameFiles']) for q in old['states'])==100
assert len({n for q in old['states'] for n in q['frameFiles']})==28
(O/'family-manifest.json').write_text(json.dumps(old,indent=2)+'\n')
for p in [O/'assembly-provenance.json',B/'sources/opposite-ns-01.request.json']:
    r=json.loads(p.read_text());r.update(familyStates=16,familySlots=100,uniqueSwimmingFigures=28)
    p.write_text(json.dumps(r,indent=2)+'\n')
print('Complete private water-turn coverage:16states/100slots/28unique swimming figures; art unaccepted.')
