"""Non-installed whole-source candidate, fixed inherited inverse ruler."""
from pathlib import Path
import json, copy, runpy, hashlib
import numpy as np
from PIL import Image, ImageDraw

P=Path(__file__).resolve().parent;R=P.parents[1]
helpers=runpy.run_path(str(R/'character/james-lying-family-v1/build.py'))
extract,foot,head,gold=[helpers[k] for k in ['extract','foot','head','gold']]
baseline_reg=P/'baseline-registration.json'
if not baseline_reg.exists():baseline_reg.write_bytes((R/'character/james-lying-south-v1/registration.json').read_bytes())
oldreg=json.loads(baseline_reg.read_text())
scale=oldreg['fixedScale']
baseline_pack=P/'baseline-bare-manifest.json'
if not baseline_pack.exists():baseline_pack.write_bytes((R/'character/james-rest-material-continuity-v1/bare-manifest.json').read_bytes())
original=json.loads(baseline_pack.read_text())
old={s['id']:s for s in original['states'] if s['id'].endswith('-south')}
oldfolder=R/'character/james-rest-material-continuity-v1'
master=Image.open(oldfolder/old['lie-down-south']['frameFiles'][0]).convert('RGBA')
cells=extract(P/'source-v2.png');assert len(cells)==12
target=foot(master);rows=[];tracking=[]
for i,(cell,box) in enumerate(cells):
    at=np.rint(target-foot(cell)*scale).astype(int)
    im=Image.new('RGBA',(256,256))
    im.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),tuple(at))
    point,hb=head(im,'south',i)
    if i>=6:
        delta=np.rint(np.array(tracking[5]['headAnchor'])-point).astype(int)
        aligned=Image.new('RGBA',(256,256));aligned.alpha_composite(im,tuple(delta));im=aligned
        at+=delta;point,hb=head(im,'south',i)
    rows.append(im)
    tracking.append({'sourceBox':box,'translation':at.tolist(),'headAnchor':point.tolist(),'protectedHeadBox':hb})
# Original fixed matte curve; then one unique-interior pooled material correction.
for i,im in enumerate(rows):
    a=np.array(im);rgb=a[:,:,:3].astype(float);x0,y0,x1,y1=tracking[i]['protectedHeadBox']
    protect=np.zeros(a.shape[:2],bool);protect[y0:y1,x0:x1]=True
    gm=gold(a,tracking[i]['protectedHeadBox']);body=(a[:,:,3]>0)&~protect&~gm
    lum=rgb.mean(2);mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170])
    factor=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);rgb[body]*=factor[body,None]
    a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');rows[i]=Image.fromarray(a)
def masks(im,box):
    a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1)
    protect=np.zeros(a.shape[:2],bool);x0,y0,x1,y1=box;protect[y0:y1,x0:x1]=True
    opaque=a[:,:,3]>240;gm=opaque&~protect&(r-b>35)&(g-b>20)
    neutral=opaque&~protect&~gm&(np.ptp(rgb,2)<28)&(rgb.mean(2)>20)&(rgb.mean(2)<110)&~((r-b>12)&(r-g>5))
    return {'gold':gm,'neutral':neutral}
_,masterbox=head(master,'south',0);mm=masks(master,masterbox);gains={}
for material in ['neutral','gold']:
    values=np.concatenate([np.array(rows[i])[:,:,:3][masks(rows[i],tracking[i]['protectedHeadBox'])[material]] for i in [1,2,3,4,5,7,8,9,10]])
    source=np.median(values,0);target_median=np.median(np.array(master)[:,:,:3][mm[material]],0)
    gains[material]={'sourceMedian':source.tolist(),'masterMedian':target_median.tolist(),'fixedGain':(target_median/source).tolist()}
for i,im in enumerate(rows):
    a=np.array(im);regions=masks(im,tracking[i]['protectedHeadBox'])
    for material,mask in regions.items():
        a[:,:,:3][mask]=np.rint(a[:,:,:3][mask].astype(float)*gains[material]['fixedGain']).clip(0,255).astype('uint8')
    rows[i]=Image.fromarray(a)
rows[0]=master.copy();rows[6]=rows[5].copy();rows[11]=rows[5].copy()
pack={k:copy.deepcopy(v) for k,v in original.items() if k!='states'}
status=json.loads((P/'selection.json').read_text()).get('status','staged_whole_source_identity_review_pending') if (P/'selection.json').exists() else 'staged_whole_source_identity_review_pending'
pack.update(name='James South compact-head whole-source candidate',status=status,states=[])
for action,poses in [('lie-down',list(range(6))),('sleep',[5,7,8,9,10,5]),('get-up',list(reversed(range(6))))]:
    state=copy.deepcopy(old[action+'-south']);state['frameFiles']=[]
    for j,i in enumerate(poses):
        path=P/'frames'/action/f'{j:03}.png';path.parent.mkdir(parents=True,exist_ok=True);rows[i].save(path);state['frameFiles'].append(path.relative_to(P).as_posix())
    state['provenance']={'source':'source-v2.png','prompt':'prompt-v2.txt','sourcePoses':poses,'fixedScale':scale,'derivation':'Complete revised source figures; inherited fixed inverse ruler, exact master arrival, pooled shared material transform, shared sleep neutral, reverse get-up. No isolated head shrinking or pose-wise scale fitting.'}
    if action=='sleep':state['restHeadOffset']=((np.array(tracking[5]['headAnchor'])-[128,224])*65.28/148).tolist()
    pack['states'].append(state)
(P/'bare-manifest.json').write_text(json.dumps(pack,indent=2)+'\n')
reg={'source':'source-v2.png','sourceSha256':hashlib.sha256((P/'source-v2.png').read_bytes()).hexdigest(),'fixedScale':scale,'tracking':tracking,'gains':gains,'runtimeInstalled':False}
(P/'registration-v2.json').write_text(json.dumps(reg,indent=2)+'\n')
board=Image.new('RGB',(7*256,3*280),'#303b40');d=ImageDraw.Draw(board)
for action_i,action in enumerate(['lie-down','sleep','get-up']):
    poses=next(s for s in pack['states'] if s['id']==action+'-south')['provenance']['sourcePoses']
    for col,i in enumerate([0,*poses]):
        im=master if col==0 else rows[i];at=(col*256,action_i*280+24);board.paste(im,at,im);d.text((at[0]+4,at[1]-20),'master' if col==0 else action+' '+str(col-1),fill='white')
board.save(P/'all-candidate-poses.png')
heads=Image.new('RGB',(6*224,3*250),'#303b40');hd=ImageDraw.Draw(heads)
for row in range(3):
    for i in range(6):
        if row==0:im=master;box=oldreg['tracking'][0]['protectedHeadBox']
        elif row==1:im=Image.open(oldfolder/old['lie-down-south']['frameFiles'][i]).convert('RGBA');box=oldreg['tracking'][i]['protectedHeadBox']
        else:im=rows[i];box=tracking[i]['protectedHeadBox']
        cx=(box[0]+box[2])//2;cy=(box[1]+box[3])//2;crop=im.crop((cx-25,cy-25,cx+25,cy+25)).resize((200,200),Image.Resampling.NEAREST)
        at=(i*224,row*250);heads.paste(crop,(at[0],at[1]+28),crop);hd.text((at[0]+4,at[1]+4),['exact master','current selected','candidate v2'][row]+' '+str(i),fill='white')
heads.save(P/'head-comparison-v2.png')
preview=[]
for i in range(6):
    b=Image.new('RGB',(512,280),'#303b40');d=ImageDraw.Draw(b)
    oldim=Image.open(oldfolder/old['lie-down-south']['frameFiles'][i]).convert('RGBA')
    for col,(label,im) in enumerate([('current selected',oldim),('candidate v2',rows[i])]):b.paste(im,(col*256,24),im);d.text((col*256+4,4),label+' '+str(i),fill='white')
    preview.append(b)
preview[0].save(P/'lie-down-comparison-v2.gif',save_all=True,append_images=preview[1:],duration=old['lie-down-south']['frameDurationsMs'],loop=0,disposal=2)
print(json.dumps({'candidateReferences':18,'fixedScale':scale,'runtimeInstalled':False,'states':[s['id'] for s in pack['states']]}))
runpy.run_path(str(P/'override_sleep.py'))
