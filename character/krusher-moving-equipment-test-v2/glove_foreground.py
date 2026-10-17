import numpy as np
from scipy.ndimage import label,binary_dilation

def glove_foreground(rgba,direction):
    rgb=rgba[:,:,:3].astype(float);yy,xx=np.mgrid[:184,:184]
    bright=(rgba[:,:,3]>180)&(rgb.mean(2)>75)&(rgb.max(2)-rgb.min(2)<23)&(yy>70)&(yy<105)&(xx>55)&(xx<128)
    if direction in ['south','north']:bright&=abs(xx-92)>17
    labs,n=label(bright);foreground=np.zeros((184,184),bool);cuffs=[]
    for k in range(1,n+1):
        y,x=np.where(labs==k)
        if len(x)<14 or x.max()-x.min()<4:continue
        centre=np.array([x.mean(),y.mean()]);points=np.stack([x,y],axis=1)-centre
        values,vectors=np.linalg.eigh(points.T@points)
        tangent=vectors[:,np.argmax(values)];normal=np.array([-tangent[1],tangent[0]])
        if normal[1]<0:normal=-normal
        dx=xx-centre[0];dy=yy-centre[1];t=dx*tangent[0]+dy*tangent[1];depth=dx*normal[0]+dy*normal[1]
        region=(abs(t)<8)&(depth>-2)&(depth<18)
        # Gloves are neutral/green dark material; trousers are cooler blue.
        glove_colour=((rgb[:,:,1]>=rgb[:,:,0])&(rgb[:,:,1]>=rgb[:,:,2])&(rgb.mean(2)<80))|(rgb.max(2)<22)
        glove=region&glove_colour&(rgba[:,:,3]>100)
        glove=binary_dilation(glove,iterations=1)&region&(rgba[:,:,3]>0)
        foreground|=glove|(labs==k)
        cuffs.append({'centre':centre.round(2).tolist(),'normal':normal.round(3).tolist(),'pixels':int((labs==k).sum())})
    return foreground,cuffs
