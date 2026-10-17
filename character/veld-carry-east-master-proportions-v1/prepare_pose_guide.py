from pathlib import Path
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
from PIL import Image
P=Path(__file__).resolve().parent
names=['near-support-v1-density-guide.png','raw-far-swing-v10.png','raw-opposite-contact-v5.png','raw-passing-v8.png','raw-swing-v9.png']
board=Image.new('RGBA',(1800,700))
for i,name in enumerate(names):
 im=Image.open(P/name).convert('RGBA');a=np.array(im);ids,_=label(a[:,:,3]>200);sizes=np.bincount(ids.ravel());sizes[0]=0;n=sizes.argmax();y,x=find_objects(ids)[n-1]
 a[~binary_dilation(ids==n,iterations=2)]=0
 crop=Image.fromarray(a).crop((max(0,x.start-2),max(0,y.start-2),min(im.width,x.stop+2),min(im.height,y.stop+2)))
 scale=min(330/crop.width,650/crop.height)
 crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
 board.alpha_composite(crop,(i*360+(360-crop.width)//2,680-crop.height))
board.save(P/'five-phase-geometry-guide.png')
