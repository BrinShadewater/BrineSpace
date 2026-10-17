from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;raw=P/'generated-death-heads.png';im=Image.open(raw).convert('RGBA');a=np.array(im);h,w=a.shape[:2];proof={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,col,row,size in [('death-east-closed',0,0,(31,33)),('death-west-closed',1,0,(31,33)),('death-quarter-closed',0,1,(28,33)),('death-south-bowed-closed',1,1,(24,33))]:
 x0,y0=col*w//2,row*h//2;x1,y1=(col+1)*w//2,(row+1)*h//2;labs,n=label(a[y0:y1,x0:x1,3]>100);largest=np.bincount(labs.ravel())[1:].argmax()+1;ys,xs=np.where(labs==largest);box=[x0+int(xs.min()),y0+int(ys.min()),x0+int(xs.max()+1),y0+int(ys.max()+1)];head=im.crop(box).resize(size,Image.Resampling.NEAREST);out=P/'sources'/f'bare-{name}-native.png';head.save(out)
 proof[name]={'raw':raw.name,'rawHash':sha(raw),'box':box,'size':list(size),'bare':out.relative_to(P).as_posix(),'bareHash':sha(out)}
 crop=[12,4,31,28] if 'east' in name else [0,4,19,28] if 'west' in name else [0,0,size[0],size[1]-4];out=P/'sources'/f'visor-{name}-native.png';head.crop(crop).save(out);proof[name]['visor']={'nativeCrop':crop,'output':out.relative_to(P).as_posix(),'hash':sha(out)}
(P/'death-head-extraction.json').write_text(json.dumps({'method':'Four isolated authored raw-alpha components; alpha preserved, uniform nearest native extraction. Visor crop omits ring/neck. Quarter source retained as fitting reference, unused in current cardinal poses.','regions':proof},indent=2)+'\n');print(json.dumps({'sources':len(proof),'rawSize':im.size}))
