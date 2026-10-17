from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,shutil
from scipy import ndimage
P=Path(__file__).resolve().parent;S=P/'sources';S.mkdir(exist_ok=True)
raw=Image.open(P/'generated-clean-heads.png').convert('RGBA');records={};scale=29/423
for i,d in enumerate(['south','east','north','west']):
    cell=raw.crop((i*raw.width//4,0,(i+1)*raw.width//4,raw.height));a=np.array(cell)
    labels,count=ndimage.label(a[:,:,3]>240);sizes=np.bincount(labels.ravel());sizes[0]=0;keep=labels==sizes.argmax()
    a[~keep]=0;box=Image.fromarray(keep.astype('uint8')*255).getbbox();part=Image.fromarray(a).crop(box)
    size=tuple(round(v*scale) for v in part.size);head=part.resize(size,Image.Resampling.NEAREST);file=S/f'clean-bare-{d}-native.png';head.save(file)
    records[d]={'cell':i,'alphaBox':box,'sourceSize':part.size,'uniformScale':scale,'nativeSize':size,'output':file.relative_to(P).as_posix(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
shutil.copyfile(P.parent/'krusher-head-fit-v4/sources/visor-lining-native.png',S/'visor-lining-native.png')
(P/'clean-extraction.json').write_text(json.dumps({'source':'generated-clean-heads.png','method':'Primary authored opaque-alpha component per quarter; shared uniform nearest export; no invented RGB or separate-axis fitting. Low-opacity cutout halos excluded.','regions':records},indent=2)+'\n')
print(json.dumps({d:q['nativeSize'] for d,q in records.items()}))
