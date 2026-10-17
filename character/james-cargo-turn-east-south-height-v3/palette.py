"""Fixed south-master material correction. Never changes alpha or pose geometry."""
import numpy as np
from PIL import Image

def match_master(image):
 a=np.array(image);rgb=a[:,:,:3].astype(float)
 r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2])
 top=np.where(a[:,:,3]>180)[0].min()
 # Preserve the entire face/hair region. Gold upper patches and belt tool are
 # calibrated separately; warm neutral knee plates must receive the matte curve.
 gold=(r-b>35)&(g-b>20)&(yy>top+30)&(yy<top+86)
 body=(a[:,:,3]>0)&(yy>top+30)&~gold
 lum=rgb.mean(2)
 mapped=np.interp(lum,[0,50,70,90,120,160,200,255],
                          [0,50,68,80,99,126,149,170])
 gain=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0)
 rgb[body]*=gain[body,None]
 # Fixed family gold gain from turn-material-audit.json; preserve geometry and alpha.
 rgb[gold]*=np.array([.7298,.816,1.026])
 a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8')
 return Image.fromarray(a)
