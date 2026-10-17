"""Pair registered south bodies with shared heads and exact new loop joins."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;R=H.parents[1];cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text());trial=json.loads((H/'bare-loop-trial-checks.json').read_text());curves=trial['curves'];checks=0;records=[];rows={v:{} for v in ['bare','helmet']}
headRecipe=json.loads((H/'head-component-selection.json').read_text());upright=Image.open(R/'character/veld-shared-helmet-south-v1/fitted-helmet.png').convert('RGBA');prone=Image.open(R/'character/veld-water-master-audit-v1/fitted-swim-south-head.png').convert('RGBA')
def skin(a):
 v=a[:,:,:3].astype(float);return (a[:,:,3]>150)&(v[:,:,0]>90)&(v[:,:,0]>v[:,:,1]*1.18)&(v[:,:,1]>v[:,:,2]*1.1)
def equip(bare,head,faceBottom,kind):
 global checks
 ha=np.array(head);sl,sn=label(skin(ha));sc=np.bincount(sl.ravel());y,x=np.where(sl==(1+np.argmax(sc[1:])));hp=(111,round(faceBottom-int(y.max())));clear=(113,105 if kind=='tread' else hp[1]-3,143,round(faceBottom)+2)
 before=np.array(bare);out=bare.copy();out.paste((0,0,0,0),clear);out.alpha_composite(head,hp);a=np.array(out);Y,X=np.indices(before.shape[:2]);v=before[:,:,:3].astype(int)
 fg=(before[:,:,3]>200)&(np.ptp(v,axis=2)<25)&(Y>=faceBottom-2)&(Y<faceBottom+10)&(X>=111)&(X<146)
 if kind!='tread':a[fg]=before[fg]
 protected=np.ones(before.shape[:2],bool);protected[clear[1]:clear[3],clear[0]:clear[2]]=False;protected[hp[1]:hp[1]+head.height,hp[0]:hp[0]+head.width]=False;assert np.array_equal(before[protected],a[protected]);checks+=1
 return Image.fromarray(a),{'helmetPosition':list(hp),'clear':list(clear),'foregroundPixels':int(fg.sum()) if kind!='tread' else 0}
def contain(im):
 global checks
 a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
for kind in ['tread','swim']:
 bareRows=[];helmetRows=[]
 for i in range(6):
  rec=next(v for v in trial['records'] if v['kind']==kind and v['slot']==i);bare=Image.open(H/rec['file']).convert('RGBA');faceBottom=rec['sourceFaceBottom']*rec['scale']+rec['position'][1];helmet,fit=equip(bare,upright if kind=='tread' else prone,faceBottom,kind);contain(bare);contain(helmet);bareRows.append(bare);helmetRows.append(helmet);records.append({'state':kind+'-south','slot':i,'faceBottom':faceBottom,**fit})
 rows['bare'][kind+'-south']=bareRows;rows['helmet'][kind+'-south']=helmetRows
source=R/'character/veld-water-material-v2/south-transition-source-v1.png';a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);counts=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:counts[k],reverse=True)[:4];ids.sort(key=lambda k:np.where(lab==k)[1].mean());launch={v:[rows[v]['tread-south'][0]] for v in rows}
for i,k in enumerate(ids):
 y,x=np.where(lab==k);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;raw=Image.fromarray(cut).crop(box);ar=np.array(raw);v=ar[:,:,:3].astype(float);s=(ar[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12);sl,sn=label(s);sc=np.bincount(sl.ravel());y,x=np.where(sl==(1+np.argmax(sc[1:])));headX=float(np.median(x));bottom=int(y.max());scale=.18;faceBottom=[134,143,150,154][i]
 masks={'cloth':(ar[:,:,3]>200)&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),'patch':(ar[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35),'skin':sl==(1+np.argmax(sc[1:]))}
 for key,m in masks.items():
  curve=curves[key]
  for c in range(3):ar[m,c]=np.interp(v[m].mean(1),curve['knots'],np.array(curve['targets'])[:,c]).clip(0,255).astype('uint8')
 pose=Image.fromarray(ar).resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);pos=(round(128-headX*scale),round(faceBottom-bottom*scale));bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos);head=Image.open(R/headRecipe['interiors'][i]['path']).convert('RGBA');helmet,fit=equip(bare,head,faceBottom,'pitch');contain(bare);contain(helmet)
 for variant,im in [('bare',bare),('helmet',helmet)]:launch[variant].append(im)
 records.append({'state':'swim-start-south','slot':i+1,'sourceBox':box,'scale':scale,'sourceFaceCentre':headX,'sourceFaceBottom':bottom,'bodyPosition':list(pos),'faceBottom':faceBottom,**fit})
for variant in rows:
 launch[variant].append(rows[variant]['swim-south'][0]);rows[variant]['swim-start-south']=launch[variant];rows[variant]['swim-stop-south']=list(reversed(launch[variant]));states=[]
 for key,poses in rows[variant].items():
  src=json.loads((R/cov['selected'][variant][key]['manifest']).read_text());state=next(v for v in src['states'] if v['id']==key).copy();files=[]
  for i,im in enumerate(poses):
   path=f'frames/{variant}/{key}/{i:03}.png';(H/path).parent.mkdir(parents=True,exist_ok=True);im.save(H/path);files.append(path)
  state['frameFiles']=files;states.append(state)
 m={**src,'name':'Veld coherent south water '+variant,'frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'states':states,'status':'staged_family_pending_visual_acceptance'};(H/f'{variant}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
for name,tracks in [('loops-master-v1',[('bare','tread-south'),('helmet','tread-south'),('bare','swim-south'),('helmet','swim-south')]),('launch-master-v1',[('bare','swim-start-south'),('helmet','swim-start-south')])]:
 sheet=Image.new('RGBA',(1536,len(tracks)*280),'#202a30');d=ImageDraw.Draw(sheet)
 for row,(variant,key) in enumerate(tracks):
  for i,im in enumerate(rows[variant][key]):sheet.alpha_composite(im,(i*256,row*280+24));d.text((i*256+4,row*280+4),variant+' '+key+' / '+str(i),fill='white')
 sheet.save(H/(name+'.png'))
(H/'family-fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'installed':False,'records':records,'nearProneHead':'exact master reuse','scaleHypotheses':{'loops':.21,'interiors':.18}},indent=2)+'\n',encoding='utf-8');print(f'{checks} protected-body/border checks PASS; paired8-state/48-frame south family composed.')
