"""Extract the edited atlas without its connected soft alpha skirt.

The edit has a separately measured source ruler. Its material authority remains
the frozen primary grade, rather than fitting a new curve to the alpha halo.
"""
import numpy as np
from PIL import Image
from scipy.ndimage import label

def prepare(path,heads,curve):
    raw=np.array(Image.open(path).convert('RGBA'));rgb=raw[:,:,:3].astype(float)
    yy,xx=np.indices(raw.shape[:2]);labs,_=label(raw[:,:,3]>240)
    counts=np.bincount(labs.ravel());counts[0]=0
    ids=sorted(np.argsort(counts)[-6:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
    mapped=np.interp(rgb.mean(2),curve['neutralInput'],curve['neutralOutput'])
    weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
    grade=raw.copy();grade[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8')
    hair=np.zeros(raw.shape[:2],bool);patch=hair.copy()
    for hx,hy in heads:
        hair|=(abs(xx-hx)<43*1.4)&(yy>=hy)&(yy<hy+65*1.4)
        patch|=(abs(xx-hx)<115*1.4)&(yy>hy+65*1.4)&(yy<hy+160*1.4)
    hair&=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(rgb.mean(2)<110)&(raw[:,:,3]>200)
    patch&=(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])&(raw[:,:,3]>200)
    for name,mask in [('hair',hair),('burgundy',patch)]:
        grade[mask,:3]=np.clip(rgb[mask]*np.array(curve['gains'][name]),0,255).astype('uint8')
    return raw,labs,ids,grade,curve
