from pathlib import Path
from PIL import Image
import numpy as np
from scipy.ndimage import label
P=Path(__file__).resolve().parent
for name,count in [('walk-v1.png',6),('walk-half-v3.png',3)]:
 a=np.array(Image.open(P/'sources'/name));labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
 ids=sorted(np.argsort(sizes)[-count:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
 print(name)
 for k in ids:
  y,x=np.where(labs==k);print([int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)])
