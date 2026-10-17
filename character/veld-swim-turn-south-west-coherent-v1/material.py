from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import label
H=Path(__file__).resolve().parent;R=H.parents[1]
def masks(a):
 v=a[:,:,:3].astype(float);skin=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12);lab,n=label(skin);counts=np.bincount(lab.ravel());assert n>0;skin=lab==(1+np.argmax(counts[1:]));y,x=np.where(skin);fb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];w=fb[2]-fb[0];Y,X=np.indices(a.shape[:2]);head=(X>fb[0]-w*.6)&(X<fb[2]+w*.6)&(Y>fb[1]-w*1.8)&(Y<fb[3]+2)
 return {'skin':skin,'cloth':~head&(a[:,:,3]>200)&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),'patch':~head&(a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)},fb,head
def family_curves():
 values={k:[] for k in ['skin','cloth','patch']};targets={k:[] for k in values}
 for i in [1,2,3]:
  a=np.array(Image.open(H/f'source-crops/{i:03}.png').convert('RGBA'));m,_,_=masks(a)
  for k in values:values[k].extend(a[:,:,:3][m[k]])
 for direction in ['south','west']:
  a=np.array(Image.open(R/f'character/veld-water-{direction}-coherent-v1/frames/bare/swim-{direction}/000.png').convert('RGBA'));m,_,_=masks(a)
  for k in values:targets[k].extend(a[:,:,:3][m[k]])
 q=[0,15,35,55,75,90,100];return {k:{'knots':np.percentile(np.mean(values[k],axis=1),q).tolist(),'targets':np.percentile(targets[k],q,axis=0).tolist()} for k in values}
def grade(raw,curves):
 a=np.array(raw);before=a.copy();v=a[:,:,:3].astype(float);m,fb,head=masks(a)
 for k,mask in m.items():
  for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curves[k]['knots'],np.array(curves[k]['targets'])[:,c]).clip(0,255).astype('uint8')
 union=m['skin']|m['cloth']|m['patch'];assert np.array_equal(before[~union],a[~union]);assert np.array_equal(before[:,:,3],a[:,:,3]);assert np.array_equal(before[head&~m['skin']],a[head&~m['skin']]);return Image.fromarray(a),fb,m
