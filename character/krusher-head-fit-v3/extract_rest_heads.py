from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;raw=P/'generated-rest-heads.png';im=Image.open(raw).convert('RGBA');a=np.array(im);h,w=a.shape[:2];proof={}
for name,col,row,size in [('rest-east-closed',0,0,(31,33)),('rest-west-closed',1,0,(31,33)),('rest-south-raised-closed',0,1,(26,33)),('rest-south-raised-open',1,1,(26,33))]:
 x0,y0=col*w//2,row*h//2;x1,y1=(col+1)*w//2,(row+1)*h//2;labs,n=label(a[y0:y1,x0:x1,3]>100);largest=np.bincount(labs.ravel())[1:].argmax()+1;ys,xs=np.where(labs==largest);box=[x0+int(xs.min()),y0+int(ys.min()),x0+int(xs.max()+1),y0+int(ys.max()+1)];head=im.crop(box).resize(size,Image.Resampling.NEAREST);out=P/'sources'/f'bare-{name}-native.png';head.save(out)
 proof[name]={'raw':raw.name,'rawHash':hashlib.sha256(raw.read_bytes()).hexdigest(),'box':box,'size':list(size),'bare':out.relative_to(P).as_posix(),'bareHash':hashlib.sha256(out.read_bytes()).hexdigest()}
 crop=[12,4,31,27] if 'east' in name else [0,4,19,27] if 'west' in name else [1,1,25,27];visor=head.crop(crop);out=P/'sources'/f'visor-{name}-native.png';visor.save(out);proof[name]['visor']={'nativeCrop':crop,'output':out.relative_to(P).as_posix(),'hash':hashlib.sha256(out.read_bytes()).hexdigest()}
(P/'rest-head-extraction.json').write_text(json.dumps({'method':'Four isolated raw-alpha authored components, nearest native extraction, alpha retained. Recorded face crops omit neck/ring for visor; no anatomy edits.','regions':proof},indent=2)+'\n');print(json.dumps({'sources':len(proof),'rawSize':im.size}))
