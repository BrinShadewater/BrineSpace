from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import label
p=Path(__file__).parent/'sources/drink-v1.png'
a=np.array(Image.open(p).convert('RGBA')); labs,_=label(a[:,:,3]>180); n=np.bincount(labs.ravel());n[0]=0
ids=sorted(np.argsort(n)[-6:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
print('size',a.shape)
for k in ids:
 y,x=np.where(labs==k);top=x[y<y.min()+12];print('box',[int(x.min()),int(y.min()),int(x.max()),int(y.max())],'head',[int(np.median(top)),int(y.min())],'height',int(y.max()-y.min()+1))
