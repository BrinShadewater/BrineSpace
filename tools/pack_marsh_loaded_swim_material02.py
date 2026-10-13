"""Whole-cell diagnostic packing; one neutral scale, no independent body/case fits."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';S=B/'sources';O=B/'east-loop-02-unselected';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((S/'east-loop-02.request.json').read_text())
assert sha(S/'east-loop-02.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
def binary(im):
    a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);return Image.fromarray(a)
raw=Image.open(S/'east-loop-02.raw.png').convert('RGBA');a=np.array(raw)[:,:,3]
xs=np.flatnonzero(np.sum(a>=128,axis=0)>=2);groups=np.split(xs,np.flatnonzero(np.diff(xs)>8)+1);assert len(groups)==5
edges=[0]+[round((groups[i].max()+groups[i+1].min())/2) for i in range(4)]+[raw.width]
cuts=[(edges[i],0,edges[i+1],raw.height) for i in range(5)]
cells=[binary(raw.crop(c)) for c in cuts];neutral=cells[-1].getbbox();scale=147/(neutral[3]-neutral[1]);frames=[];records=[]
for i,c in enumerate(cells):
    dense=binary(c.resize((round(c.width*scale),round(c.height*scale)),Image.Resampling.BOX));b=dense.getbbox()
    if i==4:
        offset=(round(112-(b[0]+b[2]-1)/2),172-b[3]);method='whole neutral occupied midpoint / sole bottom'
    else:
        aa=np.array(dense)[:,:,3];right_start=b[0]+round((b[2]-b[0])*.6)
        ys,xs=np.nonzero(aa[:,right_start:b[2]]>=128);assert len(ys)>0
        offset=(163-b[2],108-int(ys.min()));method='whole swim translation: case-right163 and forward-head top108; diagnostic only'
    f=Image.new('RGBA',(224,208));f.alpha_composite(dense,offset)
    assert np.count_nonzero(np.array(f)[:,:,3])==np.count_nonzero(np.array(dense)[:,:,3]),'opaque clipping'
    name=f'{i:03}.png' if i<4 else 'ruler.png';f.save(O/name);bb=f.getbbox();frames.append(f)
    records.append({'file':name,'sourceCell':cuts[i],'wholeTranslation':offset,'registration':method,'occupiedBounds':bb,'occupiedSize':[bb[2]-bb[0],bb[3]-bb[1]],'sha256':sha(O/name)})
board=Image.new('RGB',(224*6,238),'#293b40');d=ImageDraw.Draw(board)
idle=Image.open(ROOT/'character/marsh-v2/frames/bare/idle-east/000.png').convert('RGBA')
for i,im in enumerate(frames+[idle]):
    board.paste(im,(224*i,25),im);d.text((224*i+4,5),'new '+str(i) if i<4 else 'neutral' if i==4 else 'selected master',fill='white')
board.save(O/'whole-study-comparison.png')
(O/'recipe.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'rawSha256':r['rawSha256'],'generationId':r['generationId'],'neutralTargetHeight':147,'commonNeutralScale':scale,'records':records,'operations':'Five whole alpha128 cells with observed unequal columns, one neutral147 BOX scale; integer whole translations; no opaque clipping/mirror/patch/recolour/perposefit. Diagnostic swim registration is not world root/contact acceptance. No manifest/admission: head proportions need whole-source correction.'},indent=2)+'\n')
print(json.dumps({'scale':scale,'sizes':[q['occupiedSize'] for q in records],'runtimeChanged':False}))
