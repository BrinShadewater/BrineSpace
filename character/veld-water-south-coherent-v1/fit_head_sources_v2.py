"""Calibrate source helmet width and shared grade; record projection gaps before selecting."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;R=H.parents[1];records=[];checks=0
refs=[R/'character/veld-shared-helmet-south-v1/fitted-helmet.png',R/'character/veld-water-master-audit-v1/fitted-swim-south-head.png']
raw=np.array(Image.open(H/'helmet-pitch-source-v2.png').convert('RGBA'));lab,n=label(raw[:,:,3]>160);counts=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:counts[k],reverse=True)[:4];ids.sort(key=lambda k:np.where(lab==k)[1].mean())
def material(a,key):
 v=a[:,:,:3].astype(float);skin=(v[:,:,0]>90)&(v[:,:,0]>v[:,:,1]*1.18)&(v[:,:,1]>v[:,:,2]*1.12)
 neutral=(np.ptp(v,axis=2)<38)&(v.mean(2)>20)&~((v.mean(2)>205)&(v[:,:,2]>=v[:,:,0]))
 return (a[:,:,3]>200)&(skin if key=='skin' else neutral)
q=[0,15,35,55,75,90,100];curves={}
for key in ['skin','neutral']:
 rv=[]
 for path in refs:
  a=np.array(Image.open(path).convert('RGBA'));rv.extend(a[:,:,:3][material(a,key)])
 values=raw[:,:,:3][material(raw,key)].astype(float);curves[key]={'knots':np.percentile(values.mean(1),q),'targets':np.percentile(rv,q,axis=0)}
output=raw.copy();rgb=raw[:,:,:3].astype(float)
for key,curve in curves.items():
 mask=material(raw,key)
 for c in range(3):output[mask,c]=np.interp(rgb[mask].mean(1),curve['knots'],curve['targets'][:,c]).clip(0,255).astype('uint8')
heads=[Image.open(refs[0]).convert('RGBA')]
for i,k in enumerate(ids):
 y,x=np.where(lab==k);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];cut=output.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;im=Image.fromarray(cut).crop(box);scale=35/im.width;head=im.resize((35,round(im.height*scale)),Image.Resampling.LANCZOS);head.save(H/f'pitch-v2-head-{i+1:02}.png');assert head.width==35;checks+=1;assert head.mode=='RGBA';checks+=1;heads.append(head);records.append({'slot':i+1,'sourceBox':box,'fixedAnatomicalWidth':35,'sourceScale':scale,'height':head.height})
heads.append(Image.open(refs[1]).convert('RGBA'));sheet=Image.new('RGBA',(1080,230),'#202a30');d=ImageDraw.Draw(sheet)
for i,head in enumerate(heads):
 sheet.alpha_composite(head.resize((head.width*3,head.height*3),Image.Resampling.NEAREST),(i*180+35,75));d.text((i*180+6,15),['upright master','pitch source1','pitch source2','pitch source3','pitch source4','prone master'][i],fill='white');d.text((i*180+6,35),f'{head.width}x{head.height} / trial width fit',fill='#b1c2cc')
sheet.save(H/'helmet-source-fit-audit-v2.png')
(H/'head-source-fit-checks-v2.json').write_text(json.dumps({'checks':checks,'failures':0,'installed':False,'status':'trial_components_pending_body_camera_join_review','records':records,'curves':{k:{kk:vv.tolist() for kk,vv in v.items()} for k,v in curves.items()},'masterSizes':[list(im.size) for im in [heads[0],heads[-1]]]},indent=2)+'\n',encoding='utf-8');print(f'{checks} source component width/mode checks PASS; camera joins pending.')
