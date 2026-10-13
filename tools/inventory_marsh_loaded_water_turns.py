"""Inspect selected loaded-water turn topology and exact timing metadata."""
from pathlib import Path
import json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];cat=ROOT/'character/marsh-v2/catalog.json';selected={}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for s in json.loads(p.read_text())['states']:selected[s['id']]=(p,s)
turns=[{'id':s['id'],'manifest':p.relative_to(ROOT).as_posix(),'slots':len(s['frameFiles']),'durations':s.get('frameDurationsMs'),'loop':s.get('loop'),'first':s['frameFiles'][0],'last':s['frameFiles'][-1]} for p,s in selected.values() if s['id'].startswith('swim-carry-turn-')]
centers=[]
loops={f:Image.open(resolve(selected['swim-carry-'+f][0],selected['swim-carry-'+f][1]['frameFiles'][0])).convert('RGBA').tobytes() for f in ['east','west','north','south']}
for p,s in selected.values():
    if not s['id'].startswith('swim-carry-turn-') or len(s['frameFiles'])!=9:continue
    im=Image.open(resolve(p,s['frameFiles'][4])).convert('RGBA').tobytes()
    centers.append({'id':s['id'],'middleMatchesSelectedOldLoop0':[f for f,b in loops.items() if b==im]})
out=ROOT/'character/marsh-loaded-swim-turn-material-v1/sources/selected-turn-topology.json'
out.write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'selectedTurnStates':len(turns),'selectedTimingSlots':sum(q['slots'] for q in turns),'turns':turns,'oppositeMiddlePixelMatches':centers,'scope':'Ordered current catalogue topology and old-source pixel identity only; not new artwork acceptance.'},indent=2)+'\n')
print(json.dumps({'states':len(turns),'slots':sum(q['slots'] for q in turns),'oppositeCenters':centers}))
