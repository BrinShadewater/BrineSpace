"""Extract generated rigid-equipment surfaces; retain exact registered anatomy and alpha."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'whole-pose-join-v4/material-review';O=S/'case-review-v2';O.mkdir(exist_ok=True)
prior=json.loads((S/'case-review-v1/review-evidence.json').read_text());reg=json.loads((P/'whole-pose-join-v4/registration.json').read_text())
boxes=[(134,125,163,146),(134,125,162,145),(135,122,163,144),(136,126,165,148),(134,123,166,146),(134,126,163,147)]
claspboxes=[(146,130,157,141),(146,130,157,141),(147,127,158,138),(147,131,159,142),(146,128,159,140),(147,131,158,142)]
def region(a,box,clasp):
 x0,y0,x1,y1=box;m=np.zeros(a.shape[:2],bool);m[y0+1:y0+6,x0+2:x1-2]=True;m[y0+8:y1-2,x1-6:x1-1]=True
 cx0,cy0,cx1,cy1=clasp;m[cy0:cy1,cx0:cx1]=False;m[136:160,125:157]=False
 rgb=a[:,:,:3].astype(float);return m&(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)&(rgb.mean(2)>20)&(rgb.mean(2)<130)
generated={};bindings=[]
for phase,v,cropbox in [(2,23,(535,455,845,710)),(4,24,(615,468,930,728))]:
 row=reg['rows'][phase];raw=P/row['source'];a=np.array(Image.open(raw).convert('RGBA'));gpath=P/f'raw-case-surface-v{v}.png'
 # Generated crop material is fitted back to its exact original crop; only exposed native equipment mask will be consumed.
 g=np.array(Image.open(gpath).convert('RGBA').resize((cropbox[2]-cropbox[0],cropbox[3]-cropbox[1]),Image.Resampling.LANCZOS))
 a[cropbox[1]:cropbox[3],cropbox[0]:cropbox[2],:3]=g[:,:,:3]
 original=np.array(Image.open(raw).convert('RGBA'));ids,_=label(original[:,:,3]>200);sizes=np.bincount(ids.ravel());sizes[0]=0;n=int(sizes.argmax());a[~binary_dilation(ids==n,iterations=2)]=0
 x0,y0,x1,y1=row['sourceBox'];bounds=(max(0,x0-2),max(0,y0-2),min(a.shape[1],x1+2),min(a.shape[0],y1+2))
 piece=Image.fromarray(a).crop(bounds);piece=piece.resize((round(piece.width*row['scale']),round(piece.height*row['scale'])),Image.Resampling.LANCZOS)
 registered=Image.new('RGBA',(256,256));registered.alpha_composite(piece,tuple(row['position']));generated[phase]=np.array(registered)
 bindings.append({'phase':phase,'authoredSource':gpath.name,'authoredSHA256':hashlib.sha256(gpath.read_bytes()).hexdigest(),'originalPose':raw.name,'originalSHA256':hashlib.sha256(raw.read_bytes()).hexdigest(),'cropBounds':cropbox,'generatedDimensions':Image.open(gpath).size,'registration':row,'usage':'RGB only within exposed native lid/right case surface mask; no generated alpha/anatomy/grip/clasp consumed.'})
knots=prior['sourceLuminanceKnots'];targets=prior['masterLuminanceTargets'];frames=[];checks=0;rows=[]
master=Image.open(R/prior['master']).convert('RGBA');items=[('Held master',master)];board=Image.new('RGB',(1792,790),'#202a30');d=ImageDraw.Draw(board)
d.text((8,8),'AUTHORED HARD-CASE SURFACES: original registered body, alpha, hands and clasp protected.',fill='white')
for i in range(6):
 a=np.array(Image.open(S/f'{i:03}.png').convert('RGBA'));m=region(a,boxes[i],claspboxes[i]);out=a.copy();rgb=a[:,:,:3].astype(float)
 if i in generated:rgb[m]=generated[i][m,:3]
 lum=rgb[m].mean(1);new=np.interp(lum,knots,targets);out[m,:3]=(rgb[m]*(new/np.maximum(lum,1))[:,None]).clip(0,255).astype('uint8')
 assert np.array_equal(out[:,:,3],a[:,:,3]);checks+=1
 assert np.array_equal(out[~m],a[~m]);checks+=1
 cx0,cy0,cx1,cy1=claspboxes[i];assert np.array_equal(out[cy0:cy1,cx0:cx1],a[cy0:cy1,cx0:cx1]);checks+=1
 assert not m[136:160,125:157].any();checks+=1
 if i not in generated:assert np.array_equal(out,np.array(Image.open(S/f'case-review-v1/{i:03}.png').convert('RGBA')));checks+=1
 f=Image.fromarray(out);f.save(O/f'{i:03}.png');frames.append(f);items.append((f'Phase{i}',f))
 overlay=a.copy();overlay[m,:3]=[0,220,200];maskplate=Image.fromarray(overlay).crop((125,112,185,160)).resize((240,192),Image.Resampling.NEAREST);board.paste(maskplate,((i+1)*256+8,565),maskplate)
 rows.append({'phase':i,'maskPixels':int(m.sum()),'authoredCaseSource':i in generated,'sourceSHA256':hashlib.sha256((S/f'{i:03}.png').read_bytes()).hexdigest(),'outputSHA256':hashlib.sha256((O/f'{i:03}.png').read_bytes()).hexdigest(),'meanCaseAfter':float(out[m,:3].mean())})
for i,(name,f) in enumerate(items):
 d.text((i*256+8,32),name,fill='white');board.paste(f,(i*256,40),f);detail=f.crop((125,112,185,160)).resize((240,192),Image.Resampling.NEAREST);board.paste(detail,(i*256+8,330),detail)
board.save(O/'case-master-comparison.png');preview=[]
for f in frames:
 bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(f);preview.append(bg)
preview[0].save(O/'cycle.png',save_all=True,append_images=preview[1:],duration=140,loop=0,disposal=0,blend=0)
decoded=Image.open(O/'cycle.png');assert decoded.n_frames==6;checks+=1
for i,f in enumerate(preview):
 decoded.seek(i);assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(f));checks+=1;assert decoded.info['duration']==140;checks+=1
(O/'index.html').write_bytes((S/'case-review-v1/index.html').read_bytes().replace(b'Shared case tone; body motion and final materials remain under review.',b'Authored smooth case surfaces; original body and grip retained. Final motion remains under review.'))
(O/'review-evidence.json').write_text(json.dumps({'scope':'Staged equipment-surface source study only; no anatomy generation consumed, helmet/native/normal selection pending.','master':prior['master'],'sourceCurve':knots,'targetCurve':targets,'bindings':bindings,'rows':rows,'checks':checks,'failures':0,'cycleMs':840,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'authoredEquipmentPoses':2,'unchangedOtherPoses':4,'cycleMs':840,'meansAfter':[r['meanCaseAfter'] for r in rows]}))
