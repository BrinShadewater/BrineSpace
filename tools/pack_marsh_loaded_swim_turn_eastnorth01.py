"""Whole intermediate packing and exact endpoint assembly, with one neutral ruler."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';S=B/'sources';O=B/'east-north-01-unselected';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r= json.loads((S/'east-north-01.request.json').read_text())
assert sha(S/'east-north-01.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
original=Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96/exec-e2328df4-1aeb-4006-9e84-add2b1680951.png');rawpath=S/'east-north-01.raw.png'
if not rawpath.exists():shutil.copy2(original,rawpath)
assert sha(original)==sha(rawpath)
r.update(generationId=original.stem,originalGeneratedPath=original.as_posix(),rawSha256=sha(rawpath),status='whole source retained; packing/review provisional')
(S/'east-north-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
def binary(im):
    a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);return Image.fromarray(a)
raw=Image.open(rawpath).convert('RGBA');a=np.array(raw)[:,:,3];xs=np.flatnonzero(np.sum(a>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==4
edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(3)]+[raw.width]
cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(4)];cells=[binary(raw.crop(c)) for c in cuts];n=cells[-1].getbbox();scale=146/(n[3]-n[1])
ep=[Image.open(ROOT/q['path']).convert('RGBA') for q in r['stagedEndpoints']]
def midpoint(im):
    b=im.getbbox();return ((b[0]+b[2]-1)/2,(b[1]+b[3]-1)/2)
centers=[midpoint(im) for im in ep];frames=[];records=[]
for i,cell in enumerate(cells):
    dense=binary(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.BOX));b=dense.getbbox()
    if i<3:
        t=(i+1)/4;target=tuple(centers[0][j]+(centers[1][j]-centers[0][j])*t for j in range(2));source=midpoint(dense)
        offset=tuple(round(target[j]-source[j]) for j in range(2));name=f'intermediate-{i+1}.png';method='whole occupied midpoint interpolated between own exact endpoints; diagnostic only'
    else:offset=(round(112-(b[0]+b[2]-1)/2),172-b[3]);name='ruler.png';method='whole neutral midpoint112 / sole172'
    f=Image.new('RGBA',(224,208));f.alpha_composite(dense,offset)
    assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'opaque clipping'
    f.save(O/name);bb=f.getbbox();frames.append(f);records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'registration':method,'occupiedBounds':bb,'occupiedSize':[bb[2]-bb[0],bb[3]-bb[1]],'sha256':sha(O/name)})
paths=[ROOT/r['stagedEndpoints'][0]['path']]+[O/f'intermediate-{i}.png' for i in range(1,4)]+[ROOT/r['stagedEndpoints'][1]['path']]
turns=[]
for pair,order in [('east-north',paths),('north-east',list(reversed(paths)))]:
    state=r['selectedTurnState'].copy();state['id']='swim-carry-turn-'+pair;state['frameFiles']=['res://'+p.relative_to(ROOT).as_posix() for p in order];state['frameDurationsMs']=[60,90,100,90,60];state['loop']=False;turns.append(state)
(O/'manifest.json').write_text(json.dumps({'revision':'marsh-loaded-swim-turn-eastnorth01-staged','normalAdmission':False,'frameWidth':224,'frameHeight':208,'pivot':[112,172],'standingHeight':148,'textureFilter':'nearest','states':turns},indent=2)+'\n')
board=Image.new('RGB',(1568,238),'#293b40');d=ImageDraw.Draw(board)
master=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-north/000.png').convert('RGBA')
for i,im in enumerate([ep[0]]+frames[:3]+[ep[1],frames[-1],master]):
    board.paste(im,(224*i,25),im);d.text((224*i+4,5),['exact East02','yaw22.5 candidate','yaw45 candidate','yaw67.5 candidate','exact North04','own neutral','own North master'][i],fill='white')
board.save(O/'whole-turn-comparison.png')
(O/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'generationId':r['generationId'],'rawSha256':r['rawSha256'],'commonNeutralScale':scale,'neutralOccupiedTargetHeight':146,'records':records,'endpointPaths':r['stagedEndpoints'],'operations':'Four observed unequal alpha128 whole cells; one neutral146 BOX scale/integer whole translations/no opaque clipping/mirror/patch/recolour/per-pose fit. Exact own cardinal endpoints referenced unchanged. Reverse whole sequence for return yaw; not mirror. Diagnostic midpoint registration not physical world-root acceptance. All intermediate/endpoint anatomy/grade/case joins require review.'},indent=2)+'\n')
print(json.dumps({'scale':scale,'sizes':[q['occupiedSize'] for q in records],'states':2,'slots':10,'normalAdmission':False}))
