"""Measured material evidence, separate from visual acceptance."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
def measure(p):
    a=np.array(Image.open(p));rgb=a[:,:,:3].astype(float);l=rgb.mean(2);y,x=np.indices(l.shape);v=a[:,:,3]>200;top=y[v].min()
    n=v&(y>top+30)&((rgb.max(2)-rgb.min(2))<25)
    return {'neutralClothMedian':float(np.median(l[n&(l>20)&(l<100)])),'neutralBrightFractionOver120':float((l[n]>120).mean())}
data={'idle':measure(ROOT.parent/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png'),'samples':{}}
for key in ['pickup-east/005.png','carry-east/000.png','unload-east/003.png']:
    data['samples'][key]={'before':measure(ROOT/'review-before-matte-v5/frames'/key),'after':measure(ROOT/'frames'/key)}
(ROOT/'material-audit.json').write_text(json.dumps(data,indent=2)+'\n')
print('Material audit saved;idle cloth '+str(round(data['idle']['neutralClothMedian'],1))+';new samples '+str([round(v['after']['neutralClothMedian'],1) for v in data['samples'].values()]))
