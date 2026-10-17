"""Fixed body-neutral correction; preserves head, department colours and alpha."""
import numpy as np
from PIL import Image

def finish(im):
    a=np.array(im);rgb=a[:,:,:3].astype(float);value=rgb.mean(2)
    yy=np.indices(a.shape[:2])[0]
    weight=np.clip((32-np.ptp(rgb,axis=2))/12,0,1)*np.clip((140-value)/35,0,1)*np.clip((yy-50)/12,0,1)
    weight*=a[:,:,3]/255
    a[:,:,:3]=np.rint(rgb*(1+weight[:,:,None]*(np.array([.90,.93,.98])-1))).clip(0,255).astype('uint8')
    return Image.fromarray(a)
