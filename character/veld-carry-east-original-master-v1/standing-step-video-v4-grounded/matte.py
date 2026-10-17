"""Background alpha extraction only; whole opaque RGB is never recoloured."""
import numpy as np
from PIL import Image
from scipy import ndimage
BACKGROUND=np.array([12,18,24]); TOLERANCE=8
def extract(image):
 rgb=np.array(image.convert('RGB'));values=rgb.astype(int)
 foreground=np.max(np.abs(values-BACKGROUND),axis=2)>TOLERANCE
 labels,n=ndimage.label(foreground);counts=np.bincount(labels.ravel());counts[0]=0
 if counts.max()==0:raise AssertionError('No foreground')
 # Stable uniform background permits retaining disconnected boots/equipment.
 mask=ndimage.binary_erosion(foreground&(counts[labels]>=20),iterations=1)
 rgba=np.dstack((rgb,mask.astype('uint8')*255));rgba[~mask]=0
 return Image.fromarray(rgba)
def registered(image):
 assert image.size==(768,960),'Returned dimensions differ from frozen input plate'
 out=Image.new('RGBA',(256,256));out.alpha_composite(extract(image).resize((256,320),Image.Resampling.LANCZOS),(0,-32));return out
def metrics(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>200);top=int(y.min());hx=np.where(a[top:top+16,:,3]>128)[1];tx=np.where(a[top+34:top+79,:,3]>200)[1]
 cloth=a[top+49:top+89,105:140];rgb=cloth[:,:,:3].astype(float);m=(cloth[:,:,3]>200)&(np.ptp(rgb,axis=2)<18)&(rgb.mean(2)>20)&(rgb.mean(2)<160)
 return dict(height=int(y.max()-y.min()+1),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.min()+hx.max())/2),headTop=top,floor=int(y.max()),upperBodyWidth=int(tx.max()-tx.min()+1),clothMedian=np.median(rgb[m],axis=0).tolist())
