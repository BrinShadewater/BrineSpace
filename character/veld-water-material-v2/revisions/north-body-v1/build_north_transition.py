"""Independent rear launch anatomy, authored helmet pitch, exact loop joins."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;R=H.parents[1]
cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text())
def components(path):
 a=np.array(Image.open(path).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:4];ids.sort(key=lambda k:np.where(lab==k)[1].mean());result=[]
 for k in ids:
  y,x=np.where(lab==k);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;result.append((Image.fromarray(cut).crop(box),box))
 return result
# Rear source has different density from side atlases. Physical hair-width ruler:
# source y130,x243..337 =95px; corrected rear tread y50,x81..101 =21px.
SCALE=21/95
bodySource=H/'north-transition-source-v1.png';headSource=H/'north-transition-helmet-source-v1.png'
a=np.array(Image.open(bodySource).convert('RGBA'));rgb=a[:,:,:3].astype(float)
ref=np.array(Image.open(R/cov['selected']['bare']['idle-north']['files'][0]));rr=ref[:,:,:3].astype(float)
rm=(ref[:,:,3]>200)&(np.ptp(rr,axis=2)<22)&(rr.mean(2)>20)&(rr.mean(2)<130);rm[:59]=False
sm=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)&(rgb.mean(2)>20)&(rgb.mean(2)<130)
q=[0,15,35,55,75,90,100];knots=np.percentile(rgb[sm].mean(1),q);targets=np.percentile(rr[rm],q,axis=0)
rawBodies=components(bodySource);rawHeads=components(headSource)
# One source-family neutral curve for all helmet pitch interiors.
masterPaths=[R/'character/veld-shared-helmet-v1/fitted-north.png',R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png']
headRef=[];headVals=[]
for path in masterPaths:
 t=np.array(Image.open(path).convert('RGBA'));v=t[:,:,:3].astype(float);mask=(t[:,:,3]>200)&(v.mean(2)>15);headRef.extend(v[mask])
for im,box in rawHeads:
 t=np.array(im);v=t[:,:,:3].astype(float);mask=(t[:,:,3]>200)&(v.mean(2)>15);headVals.extend(v[mask])
hk=np.percentile(np.mean(headVals,axis=1),q);ht=np.percentile(headRef,q,axis=0)
landmarks=[(290,78,173),(819,139,228),(1371,171,249),(1924,193,268)]
body=[];helmet=[];records=[];checks=0
for variant,rows in [('bare',body),('helmet',helmet)]:
 im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(H/f'frames/{variant}/tread-north/000.png').convert('RGBA'),(36,58));rows.append(im)
for j,((raw,box),(rawHead,headBox)) in enumerate(zip(rawBodies,rawHeads)):
 a=np.array(raw);rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)&(rgb.mean(2)>20)&(rgb.mean(2)<130)
 for c in range(3):a[mask,c]=np.interp(rgb[mask].mean(1),knots,targets[:,c]).clip(0,255).astype('uint8')
 raw=Image.fromarray(a);pose=raw.resize((round(raw.width*SCALE),round(raw.height*SCALE)),Image.Resampling.LANCZOS)
 hx,hy,hbottom=landmarks[j];crown=[106,105,104,104][j];pos=(round(128-(hx-box[0])*SCALE),round(crown-(hy-box[1])*SCALE))
 bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos)
 a=np.array(rawHead);rgb=a[:,:,:3].astype(float);mask=(a[:,:,3]>0)&(rgb.mean(2)>15)
 for c in range(3):a[mask,c]=np.interp(rgb[mask].mean(1),hk,ht[:,c]).clip(0,255).astype('uint8')
 head=Image.fromarray(a).resize((33,round(rawHead.height*33/rawHead.width)),Image.Resampling.LANCZOS);head.save(H/f'north-pitch-head-{j+1:02}.png')
 hp=(112,[100,99,99,99][j]);clear=(114,crown-1,142,round(crown+(hbottom-hy)*SCALE)+1)
 equipped=bare.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(head,hp)
 b=np.array(bare);e=np.array(equipped);protected=np.ones(b.shape[:2],bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[hp[1]:hp[1]+head.height,hp[0]:hp[0]+head.width]=False
 assert np.array_equal(b[protected],e[protected]);checks+=1
 for im in [bare,equipped]:
  a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
 body.append(bare);helmet.append(equipped);records.append({'interior':j+1,'sourceBox':box,'bodyScale':SCALE,'sourceHeadLandmark':list(landmarks[j]),'position':list(pos),'bareCrown':crown,'headSourceBox':headBox,'headWidth':33,'headHeight':head.height,'helmetPosition':list(hp),'clear':list(clear)})
for variant,rows in [('bare',body),('helmet',helmet)]:
 im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(H/f'frames/{variant}/swim-north/000.png').convert('RGBA'),(36,74));rows.append(im)
 src=json.loads((R/cov['selected']['bare']['swim-start-north']['manifest']).read_text());states=[]
 for key,order in [('swim-start-north',range(6)),('swim-stop-north',range(5,-1,-1))]:
  state=next(s for s in src['states'] if s['id']==key).copy();files=[]
  for slot,index in enumerate(order):
   path=f'frames/{variant}/{key}/{slot:03}.png';(H/path).parent.mkdir(parents=True,exist_ok=True);rows[index].save(H/path);files.append(path)
  state['frameFiles']=files;states.append(state)
 manifest={**src,'name':'Veld coherent north swim transitions '+variant,'states':states,'status':'body_fit_preview_not_selected_pending_motion_repair'}
 (H/f'north-transition-{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
contact=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(contact)
for row,rows in enumerate([body,helmet]):
 for slot,im in enumerate(rows):contact.alpha_composite(im,(slot*256,row*280+24));draw.text((slot*256+4,row*280+4),('bare' if row==0 else 'helmet')+' / '+str(slot),fill='white')
contact.save(H/'north-transition-master-v1.png')
(H/'north-transition-fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'fixedAnatomicalScale':SCALE,'physicalRuler':{'sourceHairWidth':95,'sourceHairRow':130,'treadHairWidth':21,'treadHairRow':50},'bodySourceSha256':hashlib.sha256(bodySource.read_bytes()).hexdigest(),'headSourceSha256':hashlib.sha256(headSource.read_bytes()).hexdigest(),'bodyNeutralKnots':knots.tolist(),'bodyNeutralTargets':targets.tolist(),'headNeutralKnots':hk.tolist(),'headNeutralTargets':ht.tolist(),'records':records,'installed':False},indent=2)+'\n',encoding='utf-8')
print(f'{checks} protected-body/clipping checks pass; paired north transition preview; body motion pending.')
