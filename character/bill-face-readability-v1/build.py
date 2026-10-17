from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
a=np.array(Image.open(P.parent/'bill-front-rear-matte-v2/south-source-matte.png').convert('RGB'));v=a.astype(float)
y,x=np.indices(a.shape[:2]);u=x/a.shape[1];w=y/a.shape[0]
# Feathered face interior excludes scalp, ears and collar. No shape synthesis.
radius=((u-.497)/.052)**2+((w-.157)/.046)**2
mask=np.clip((1-radius)/.22,0,1)
lum=v@np.array([.2126,.7152,.0722])
# Deepen existing dark features, gently lift warm midtones, retain bright highlights.
delta=np.clip((lum-112)*.16,-9,5)*np.clip((230-lum)/35,0,1)
out=np.rint(v+mask[:,:,None]*delta[:,:,None]*np.array([1.0,.95,.88])).clip(0,255).astype('uint8')
assert np.array_equal(a[mask==0],out[mask==0])
Image.fromarray(out).save(P/'south-source.png')
(P/'face-checks.json').write_text(json.dumps({'outsideFaceUnchanged':True,'changedPixels':int(np.any(a!=out,axis=2).sum()),'maximumChannelChange':int(np.abs(out.astype(int)-a.astype(int)).max()),'method':'Feathered face-only luminance contrast, dark features at most -9, warm highlights at most +5; original geometry retained.'},indent=2))
print('Face-only correction saved; all pixels outside feathered face region identical.')
