"""Bounded master palette grade; no geometry, alpha or invented detail changes."""
import numpy as np
from PIL import Image
def apply(prepared,spec,idle_path):
    raw,labs,ids,graded,curve=prepared
    rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2]);density=spec['density']
    ref=np.array(Image.open(idle_path).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
    body=np.zeros(raw.shape[:2],bool);face=body.copy()
    for hx,hy in spec['heads']:
        body|=(abs(xx-hx)<160*density)&(yy>=hy+85*density)&(yy<hy+490*density)
        face|=(abs(xx-hx)<48*density)&(yy>=hy+23*density)&(yy<hy+78*density)
    # Cream-tinted cuffs/armor fall outside the legacy neutral-spread22 mask.
    hardware=body&(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)>22)&(np.ptp(rgb,axis=2)<60)&(rgb.mean(2)>85)&(rgb[:,:,0]<1.4*rgb[:,:,1])&(rgb[:,:,0]<1.4*rgb[:,:,2])
    authority=(ref[:,:,3]>200)&(ry>=50)&(np.ptp(rr,axis=2)<60)&(rr.mean(2)>70)&(rr[:,:,0]<1.4*rr[:,:,1])&(rr[:,:,0]<1.4*rr[:,:,2])
    q=[0,.1,.25,.5,.75,.9,.98,1]
    src=np.quantile(rgb.mean(2)[hardware],q);dst=np.quantile(rr.mean(2)[authority],q)
    mapped=np.interp(rgb.mean(2)[hardware],src,dst)
    graded[hardware,:3]=np.clip(rgb[hardware]*mapped[:,None]/rgb.mean(2)[hardware,None],0,255).astype('uint8')
    warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])
    face&=warm&(raw[:,:,3]>200)&(rgb.mean(2)>65)
    rf=(ref[:,:,3]>200)&(ry>=33)&(ry<50)&(rx<105)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65)
    gain=np.median(rr[rf],axis=0)/np.median(rgb[face],axis=0)
    graded[face,:3]=np.clip(rgb[face]*gain,0,255).astype('uint8')
    curve['boundedMaterialCorrection']={'hardwareInput':src.tolist(),'hardwareOutput':dst.tolist(),'faceGain':gain.tolist(),'hardwarePixels':int(hardware.sum()),'facePixels':int(face.sum()),'scope':'warm-grey hardware and full profile skin only; alpha/geometry unchanged'}
    return raw,labs,ids,graded,curve
