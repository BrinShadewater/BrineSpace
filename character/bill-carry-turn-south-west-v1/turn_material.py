"""Frozen endpoint-derived material grade; preserves geometry and dark outlines."""
import numpy as np
from PIL import Image

def cloth_samples(im):
 a=np.array(im);rgb=a[155:195,:,:3].astype(float)
 mask=(a[155:195,:,3]>200)&(np.ptp(rgb,axis=2)<20)
 return rgb.mean(2)[mask]

def match(frames):
 quantiles=[.1,.25,.5,.75,.9]
 source=np.quantile(np.concatenate([cloth_samples(im) for im in frames[1:-1]]),quantiles)
 target=np.mean([np.quantile(cloth_samples(im),quantiles) for im in [frames[0],frames[-1]]],axis=0)
 settings={'method':'one frozen neutral midtone lift from pooled turn cloth to both exact loaded endpoint cloth bands','quantiles':quantiles,'input':source.tolist(),'target':target.tolist(),'deltas':(target-source).tolist(),'sampleBand':[155,195],'endpointsUnchanged':True}
 output=[frames[0]];audit=[]
 for i,im in enumerate(frames[1:-1],1):
  a=np.array(im);rgb=a[:,:,:3].astype(float);luma=rgb.mean(2);spread=np.ptp(rgb,axis=2);yy,xx=np.indices(a.shape[:2])
  neutral=np.clip(1-(spread-8)/24,0,1)*(yy>=104)*(a[:,:,3]>0)
  lift=np.interp(luma,source,target-source,left=0,right=0)*neutral*.9
  a[:,:,:3]=np.clip(np.round(rgb+lift[:,:,None]),0,255).astype('uint8');a[a[:,:,3]==0]=0
  result=Image.fromarray(a);output.append(result)
  audit.append({'pose':i,'beforeMedian':float(np.median(cloth_samples(im))),'afterMedian':float(np.median(cloth_samples(result))),'alphaUnchanged':bool(np.array_equal(np.array(im)[:,:,3],a[:,:,3]))})
 output.append(frames[-1]);settings['audit']=audit;settings['correctionStrength']=.9
 return output,settings
