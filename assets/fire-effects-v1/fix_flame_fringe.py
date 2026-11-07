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

# v3 (owner playtest, Sept 15): the r-g<40 test above missed pink-grey checkerboard
# blends (r-g >= 40) that read as white cutouts in game. Peel pale residue that
# touches transparency, up to three pixels deep; the warm interior never matches.
peeled=0
for _ in range(3):
    visible=rgba[:,:,3]>0
    r,g,b=rgba[:,:,:3].astype(np.int16).transpose(2,0,1)
    pale=visible&(b>=80)&((g-b)<=25)&(r<250)
    clear=np.pad(~visible,1,constant_values=True)
    touches=clear[:-2,1:-1]|clear[2:,1:-1]|clear[1:-1,:-2]|clear[1:-1,2:]
    peel=pale&touches
    if not peel.any(): break
    rgba[peel]=0
    peeled+=int(peel.sum())
Image.fromarray(rgba).save(ROOT/'flame-atlas-v3.png')
Image.fromarray(rgba).resize((384,256),Image.Resampling.NEAREST).save(ROOT/'flame-96x128-v3.png')
print(f'v3: peeled {peeled} pale residue pixels touching transparency.')
