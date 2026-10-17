from pathlib import Path
from PIL import Image
from scipy import ndimage
import json,hashlib,numpy as np
R=Path(__file__).resolve().parent;d=json.loads((R/'manifest.json').read_text());assert len(d['states'])==52 and len(d['headings'])==8
for h,m in d['headings'].items():
 im=Image.open(R/m['pose']).convert('RGBA');assert im.size==(512,512);box=im.getbbox();assert min(box[:2])>0 and max(box[2:])<512;assert m['sourceScale']<1
 labels,n=ndimage.label(np.array(im)[:,:,3]>128);assert sum(np.bincount(labels.ravel())[1:]>30)==1,h
count=0
for key,m in d['effects'].items():
 atlas=Image.open(R/m['atlas']).convert('RGBA');assert len(m['frames'])==60
 for n,p in enumerate(m['frames']):
  im=Image.open(R/p).convert('RGBA');assert im.size==(512,512);box=im.getbbox();assert box and min(box[:2])>0 and max(box[2:])<512,(key,n,box)
  assert im.tobytes()==atlas.crop((n%6*512,n//6*512,(n%6+1)*512,(n//6+1)*512)).tobytes();count+=1
for e in d['states']:
 assert (R/e['body']).is_file();assert e['effect'] is None or e['effect'] in d['effects'];assert e['frameCount']==(120 if e['state']=='scan' else 60) and e['fps']==30
for s in d['sources']:assert hashlib.sha256((R/s['path']).read_bytes()).hexdigest()==s['sha256']
result={'clips':52,'headings':8,'effectFrames':count,'atlasParity':'pass','bodyConnectivity':'pass','bounds':'pass','noSourceUpscaling':True,'sourceHashes':'pass','gameplayIntegration':False}
(R/'review/validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
