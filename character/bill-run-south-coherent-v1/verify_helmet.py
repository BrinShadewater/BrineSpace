from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
bare=json.loads((P/'manifest.json').read_text());m=json.loads((P/'helmet-manifest.json').read_text());reg=json.loads((P/'helmet-registration.json').read_text());checks=[];hashes={};head=np.array(Image.open(P/'sources/south-canonical-helmet.png').convert('RGBA'));y,x=np.indices((256,256))
def check(ok,label):assert ok,label;checks.append(label)
check(m['states'][0]['frameDurationsMs']==bare['states'][0]['frameDurationsMs'] and m['strideDistanceCells']==bare['strideDistanceCells'],'Paired clock and stride')
for row,f in zip(reg['frames'],m['states'][0]['frameFiles']):
 a=np.array(Image.open(R/row['bareFile'][6:]).convert('RGBA'));b=np.array(Image.open(R/f[6:]).convert('RGBA'));px,py=row['position'];w,h=row['componentSize'];x0,y0,x1,y1=row['eraseRect'];region=((x>=x0)&(x<x1)&(y>=y0)&(y<y1))|((x>=px)&(x<px+w)&(y>=py)&(y<py+h))
 check(np.array_equal(a[~region],b[~region]),'Exact approved body outside bounded head')
 opaque=head[:,:,3]==255;check(np.array_equal(b[py:py+h,px:px+w][opaque],head[opaque]),'Native hardware pixels exact')
 check(row['nativeScale']==1 and row['componentSize']==[36,42],'Native selected helmet size')
 check(not b[[0,-1],:,3].any() and not b[:,[0,-1],3].any(),'Unclipped equipment plane')
 hashes[f]=hashlib.sha256((R/f[6:]).read_bytes()).hexdigest()
(P/'helmet-verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'sha256':hashes,'scope':'hardware/body/plane/clocks; biomechanical motion and owner visual acceptance separate'},indent=2)+'\n')
print(str(len(checks))+' equipment package checks pass')
