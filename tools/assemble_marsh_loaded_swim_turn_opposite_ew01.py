"""Compose whole East/West water turns through shared exact North, no new raster edits."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';O=B/'opposite-ew-01-unselected';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
def resolve(p,n):return ROOT/n.removeprefix('res://') if n.startswith('res://') else (p.parent/n).resolve()
quarterpaths=[B/'east-north-02-unselected/manifest.json',B/'west-north-01-unselected/manifest.json'];quarters={}
for p in quarterpaths:
    for state in json.loads(p.read_text())['states']:quarters[state['id']]=state
east=quarters['swim-carry-turn-east-north']['frameFiles'];west=quarters['swim-carry-turn-north-west']['frameFiles'];assert east[-1]==west[0]
forward=east+west[1:];assert len(forward)==9
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in json.loads(cat.read_text())['body']:
    p=resolve(cat,n)
    for state in json.loads(p.read_text())['states']:selected[state['id']]=(p,state)
oldmanifest,oldstate=selected['swim-carry-turn-east-west'];oldframes=[resolve(oldmanifest,n) for n in oldstate['frameFiles']]
reversemanifest,reversestate=selected['swim-carry-turn-west-east'];reverseframes=[resolve(reversemanifest,n) for n in reversestate['frameFiles']]
assert all(Image.open(p).convert('RGBA').tobytes()==Image.open(q).convert('RGBA').tobytes() for p,q in zip(reverseframes,reversed(oldframes))), 'old reverse comparison must match actual current catalogue'
durations=[60,90,100,90,120,90,100,90,60];assert oldstate['frameDurationsMs']==durations
states=[]
for pair,frames in [('east-west',forward),('west-east',list(reversed(forward)))]:
    state=selected['swim-carry-turn-'+pair][1].copy();state['frameFiles']=frames;state['frameDurationsMs']=durations;state['loop']=False;states.append(state)
manifest={'revision':'marsh-loaded-swim-opposite-ew01-staged','normalAdmission':False,'frameWidth':224,'frameHeight':208,'pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':states}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
cardinal=ROOT/'character/marsh-loaded-swim-material-v1/cardinal01-cross-review/family-manifest.json';family=json.loads(cardinal.read_text());family['revision']='marsh-loaded-swim-north-turn-family01-staged';family['states']+=list(quarters.values())+states
assert len(family['states'])==10 and sum(len(s['frameFiles']) for s in family['states'])==62
(O/'family-manifest.json').write_text(json.dumps(family,indent=2)+'\n')
board=Image.new('RGB',(2016,238),'#293b40');d=ImageDraw.Draw(board)
for i,n in enumerate(forward):
    im=Image.open(resolve(O/'manifest.json',n)).convert('RGBA');board.paste(im,(224*i,25),im);d.text((224*i+4,5),['exact East','EastNorth1','EastNorth2','EastNorth3','exact North /120ms','NorthWest1','NorthWest2','NorthWest3','exact West'][i],fill='white')
board.save(O/'whole-opposite-comparison.png')
inputs=[ref(p) for p in quarterpaths+[cardinal,oldmanifest,reversemanifest,cat]+oldframes+reverseframes+[resolve(O/'manifest.json',n) for n in forward]]
r={'normalAdmission':False,'fullGoalComplete':False,'status':'assembled whole source sequence; native/opposite joins provisional','sourceFrames':[ref(p) for p in oldframes],'selectedTurnState':oldstate,'selectedTurnManifest':ref(oldmanifest),'orderedInputs':inputs,'middle':'Exact staged North04 loop0, one120ms hold rather than two60ms copies','durationsMs':durations,'turnStates':2,'turnTimingSlots':18,'familyStates':10,'familySlots':62,'uniqueSwimmingFigures':22,'operations':'Unchanged whole EastNorth02 quarter plus unchanged whole NorthWest01 quarter, drop duplicate sharedNorth frame only; reverse entire nine-frame order for WestEast, never mirror/raster patch/rescale. Original water metadata retained; no normal catalogue selection. Physical body/case/head/root/grade/yaw joins remain provisional.'}
(O/'assembly-provenance.json').write_text(json.dumps(r,indent=2)+'\n')
(B/'sources/opposite-ew-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
print('Whole EastWest/WestEast viaNorth assembled:2states/18slots; private family10states/62slots,22swimming figures.')
