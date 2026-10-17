import numpy as np
from PIL import Image

def apply(prepared,cfg,idle_path):
 ref=np.array(Image.open(idle_path).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
 authority=(ref[:,:,3]>200)&(ry>=49)&(ry<=74)&(rr[:,:,0]>80)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])
 assert authority.any()
 for key,data in prepared.items():
  raw,labs,ids,graded,curve=data;rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2]);region=np.zeros(raw.shape[:2],bool);spec=cfg['sources'][key];density=spec['density']
  for hx,hy in spec['heads']:region|=(abs(xx-hx)<115*density)&(yy>hy+65*density)&(yy<hy+160*density)
  red=region&(raw[:,:,3]>200)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2]);sample=red&(rgb[:,:,0]>100)
  assert sample.any()
  gain=np.median(rr[authority],axis=0)/np.median(rgb[sample],axis=0)
  graded[red,:3]=np.clip(rgb[red]*gain,0,255).astype('uint8')
  curve['shoulderPlateOverride']={'gain':gain.tolist(),'sourceSampleMinRed':100,'masterSampleMinRed':80,'masterRawY':[49,74],'scope':'bounded red shoulder material; sample plate interiors rather than dark outlines; alpha unchanged'}
