from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent
path=P/'generated-cargo-quarters.png';im=Image.open(path).convert('RGBA');a=np.array(im);height,width=a.shape[:2];regions={}
for view,x,y,size in [('se',0,0,(29,33)),('sw',1,0,(29,33)),('ne',0,1,(28,32)),('nw',1,1,(28,32))]:
    x0,y0=x*width//2,y*height//2;x1,y1=(x+1)*width//2,(y+1)*height//2
    lab,n=label(a[y0:y1,x0:x1,3]>100);component=np.bincount(lab.ravel())[1:].argmax()+1;ys,xs=np.where(lab==component)
    box=[x0+int(xs.min()),y0+int(ys.min()),x0+int(xs.max()+1),y0+int(ys.max()+1)]
    head=im.crop(box).resize(size,Image.Resampling.NEAREST);target=P/'sources'/('bare-'+view+'-native.png');head.save(target)
    regions[view]={'raw':path.name,'rawHash':hashlib.sha256(path.read_bytes()).hexdigest(),'box':box,'size':list(size),'output':target.relative_to(P).as_posix(),'outputHash':hashlib.sha256(target.read_bytes()).hexdigest()}
    if view in ['se','sw']:
        # Exclude the bottom authored neck/ring for visor identity fitting.
        visor=head.crop((0,0,head.width,29));target=P/'sources'/('visor-'+view+'-native.png');visor.save(target)
        regions[view]['visor']={'nativeCrop':[0,0,head.width,29],'output':target.relative_to(P).as_posix(),'outputHash':hashlib.sha256(target.read_bytes()).hexdigest()}
(P/'cargo-quarter-extraction.json').write_text(json.dumps({'method':'Four raw-alpha isolated authored components; fixed bounding boxes, nearest native extraction, original alpha preserved. No skull or neck painting.','regions':regions},indent=2)+'\n')
print(json.dumps(regions))
