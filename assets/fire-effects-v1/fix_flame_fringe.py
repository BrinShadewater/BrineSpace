"""Remove exterior pale matte residue; retain v1 for comparison."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
from prepare import label
ROOT=Path(__file__).resolve().parent
rgba=np.array(Image.open(ROOT/'flame-atlas.png'))
r,g,b=rgba[:,:,:3].astype(np.int16).transpose(2,0,1)
possible=(rgba[:,:,3]==0)|((r-g<40)&(b>100))
labels,_=label(possible)
edges=np.unique(np.concatenate([labels[0],labels[-1],labels[:,0],labels[:,-1]]))
outside=np.isin(labels,edges[edges>0])
remove=(rgba[:,:,3]>0)&outside
rgba[remove]=0
Image.fromarray(rgba).save(ROOT/'flame-atlas-v2.png')
Image.fromarray(rgba).resize((384,256),Image.Resampling.NEAREST).save(ROOT/'flame-96x128-v2.png')
print(f'Removed {remove.sum()} exterior matte pixels; existing transparent gaps retained.')
