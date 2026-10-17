"""Fixed source proportions, planted boot registration and exact idle endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
IDLE=Path(__file__).resolve().parent.parent/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png'
def prepare(source,heads,count,density=1):
 raw=np.array(Image.open(source).convert('RGBA'));rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2]);labs,_=label(raw[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0
 ids=sorted(np.argsort(n)[-count:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
 ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22);rn=(ref[:,:,3]>200)&(ry>50)&(np.ptp(rr,axis=2)<22)
 src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[rn],q);mapped=np.interp(rgb.mean(2),src,dst);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 grade=raw.copy();grade[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8')
 hair=np.zeros(raw.shape[:2],bool);face=hair.copy();patch=hair.copy()
 for hx,hy in heads:
  hair|=(abs(xx-hx)<43*density)&(yy>=hy)&(yy<hy+40*density)
  face|=(xx>hx)&(xx<hx+45*density)&(yy>=hy+23*density)&(yy<hy+75*density)
  patch|=(xx>hx-90*density)&(xx<hx-5*density)&(yy>hy+65*density)&(yy<hy+160*density)
 warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(raw[:,:,3]>200)
 hair&=warm;face&=warm&(rgb.mean(2)>65);patch&=(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])&(raw[:,:,3]>200)
 rh=(ref[:,:,3]>180)&(ry>=24)&(ry<33)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]);rf=(ref[:,:,3]>180)&(rx>92)&(ry>=33)&(ry<50)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65);rp=(ref[:,:,3]>180)&(ry>50)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])
 gains={}
 for name,mask,authority in [('hair',hair,rh),('face',face,rf),('burgundy',patch,rp)]:
  gain=np.median(rr[authority],axis=0)/np.median(rgb[mask],axis=0);gains[name]=gain.tolist();grade[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8')
 return raw,labs,ids,grade,{"neutralInput":src.tolist(),"neutralOutput":dst.tolist(),"gains":gains}
