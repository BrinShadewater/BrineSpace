from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import numpy as np,json
P=Path(__file__).resolve().parent;R=P.parent
paths=[R/'bill-video-north-v5/master-source.png',R/'bill-land-water-north-v1/sources/crouch-canvas-v2.png',P/'sources/rise-canvas-v2.png',P/'sources/near-stand-canvas-v2.png',P/'sources/near-stand-canvas-v3.png']
out=[]
for p in paths:
 a=np.array(Image.open(p).convert('RGBA'));y,x=np.indices(a.shape[:2]);rgb=a[:,:,:3].astype(float)
 m=(a[:,:,3]>180)&(x>500)&(x<750)&(y>80)&(y<460)&(rgb[:,:,0]>rgb[:,:,1]*1.12)&(rgb[:,:,1]>rgb[:,:,2]*1.2)&(rgb[:,:,0]>35)
 labs,n=label(m);sizes=np.bincount(labs.ravel());ys,xs=np.where(labs==np.argmax(sizes[1:])+1)
 out.append(dict(file=p.relative_to(R).as_posix(),hairBox=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],width=int(xs.max()-xs.min()+1),height=int(ys.max()-ys.min()+1)))
(P/'hair-diagnostic.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out))
