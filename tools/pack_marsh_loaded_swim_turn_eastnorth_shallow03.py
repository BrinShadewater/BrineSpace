"""Retain complete shallow correction and assemble whole source banks, no part repair."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';S=B/'sources';O=B/'east-north-03-unselected';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((S/'east-north-shallow-03.request.json').read_text())
assert sha(S/'east-north-shallow-03.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-2a70319a-148b-4229-be2b-75819d1ef1cb.png');rawpath=S/'east-north-shallow-03.raw.png'
if not rawpath.exists():shutil.copy2(original,rawpath)
assert sha(original)==sha(rawpath)
r.update(generationId=original.stem,originalGeneratedPath=original.as_posix(),rawSha256=sha(rawpath),status='whole shallow correction retained; source-bank assembly/visual review pending')
(S/'east-north-shallow-03.request.json').write_text(json.dumps(r,indent=2)+'\n')
def binary(im):
    a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);return Image.fromarray(a)
raw=Image.open(rawpath).convert('RGBA');xs=np.flatnonzero(np.sum(np.array(raw)[:,:,3]>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==2
edge=round((groups[0].max()+groups[1].min())/2);cuts=[(0,0,edge,raw.height),(edge,0,raw.width,raw.height)];cells=[binary(raw.crop(c)) for c in cuts];n=cells[1].getbbox();scale=147/(n[3]-n[1]);records=[];frames=[]
ep=[Image.open(ROOT/q['path']).convert('RGBA') for q in r['stagedEndpoints']]
def midpoint(im):
    b=im.getbbox();return ((b[0]+b[2]-1)/2,(b[1]+b[3]-1)/2)
centers=[midpoint(im) for im in ep];target=tuple(centers[0][j]+(centers[1][j]-centers[0][j])*.25 for j in range(2))
for i,cell in enumerate(cells):
    dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox()
    if i==0:src=midpoint(dense);offset=tuple(round(target[j]-src[j]) for j in range(2));name='intermediate-1.png';method='whole midpoint25percent between unchanged own endpoint midpoints; diagnostic only'
    else:offset=(round(112-(b[0]+b[2]-1)/2),172-b[3]);name='ruler.png';method='whole own-East neutral midpoint112/sole172'
    f=Image.new('RGBA',(224,208));f.alpha_composite(dense,offset);assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'opaque clipping'
    f.save(O/name);bb=f.getbbox();frames.append(f);records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'registration':method,'occupiedBounds':bb,'occupiedSize':[bb[2]-bb[0],bb[3]-bb[1]],'sha256':sha(O/name)})
paths=[ROOT/r['stagedEndpoints'][0]['path'],O/'intermediate-1.png',B/'east-north-02-unselected/intermediate-2.png',B/'east-north-02-unselected/intermediate-3.png',ROOT/r['stagedEndpoints'][1]['path']];turns=[]
for pair,order in [('east-north',paths),('north-east',list(reversed(paths)))]:
    state=r['selectedTurnState'].copy();state['id']='swim-carry-turn-'+pair;state['frameFiles']=['res://'+p.relative_to(ROOT).as_posix() for p in order];state['frameDurationsMs']=[60,90,100,90,60];state['loop']=False;turns.append(state)
manifest={'revision':'marsh-loaded-swim-turn-eastnorth03-staged','normalAdmission':False,'frameWidth':224,'frameHeight':208,'pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':turns}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
family=json.loads((ROOT/'character/marsh-loaded-swim-material-v1/cardinal01-cross-review/family-manifest.json').read_text());family['revision']='marsh-loaded-swim-cardinal-plus-eastnorth03-staged';family['states']+=turns;(O/'family-manifest.json').write_text(json.dumps(family,indent=2)+'\n')
master=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png').convert('RGBA');board=Image.new('RGB',(1568,238),'#293b40');d=ImageDraw.Draw(board)
for i,im in enumerate([Image.open(p).convert('RGBA') for p in paths]+[frames[1],master]):
    board.paste(im,(224*i,25),im);d.text((224*i+4,5),['exact East02','whole shallow03','whole rear02/45','whole rear02/67.5','exact North04','own East neutral','own East master'][i],fill='white')
board.save(O/'whole-turn-comparison.png')
old=Image.open(B/'east-north-02-unselected/intermediate-1.png').convert('RGBA');board=Image.new('RGB',(1792,446),'#293b40');d=ImageDraw.Draw(board)
for i,im in enumerate([ep[0],old,frames[0],frames[1]]):
    large=im.resize((448,416),Image.Resampling.NEAREST);board.paste(large,(448*i,30),large);d.text((448*i+4,6),['Exact East02 endpoint','Whole02 shallow','Whole03 shallow correction','Own East neutral03'][i],fill='white')
board.save(O/'whole-shallow-correction-comparison.png')
(O/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'generationId':r['generationId'],'rawSha256':r['rawSha256'],'commonNeutralScale':scale,'neutralOccupiedTargetHeight':147,'records':records,'endpointPaths':r['stagedEndpoints'],'wholeIntermediateSourceParity':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in paths[1:4]],'operations':'Two alpha128 observed unequal whole cells/one own-East neutral147 BOX scale/integer whole translations/no opaque clipping/mirror/patch/recolour/per-pose fit. Entire shallow figure03 plus two entire rear figures02; unchanged own endpoint bytes and whole reverse sequence. Diagnostic midpoint not world-root acceptance.'},indent=2)+'\n')
print(json.dumps({'scale':scale,'sizes':[q['occupiedSize'] for q in records],'turnStates':2,'familyStates':6,'turnSlots':10,'familySlots':34,'normalAdmission':False}))
