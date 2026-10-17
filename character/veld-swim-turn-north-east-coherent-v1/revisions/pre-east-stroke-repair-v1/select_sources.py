"""Re-extract explicit selected cells from immutable source atlases/single pose."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;selection=json.loads((H/'source-selection-v1.json').read_text());records=[];cache={}
for index,s in enumerate(selection['selected']):
 file=s['source']
 if file not in cache:
  a=np.array(Image.open(H/file).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());count=1 if 'yaw54' in file else 4;ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:count];assert len(ids)==count;ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/2)),np.where(lab==k)[1].mean()));cache[file]=(a,lab,ids)
 a,lab,ids=cache[file];k=ids[s['sourceSlot']];y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert min(box[:2])>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0];cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;im=Image.fromarray(cut).crop(box);(H/'selected-crops').mkdir(exist_ok=True);im.save(H/f'selected-crops/{index:03}.png');records.append(dict(interiorSlot=index+1,source=file,sourceSlot=s['sourceSlot'],sourceBox=box,size=list(im.size),rawSha256=hashlib.sha256((H/file).read_bytes()).hexdigest()))
(H/'selected-extraction-v1.json').write_text(json.dumps(dict(checks=len(records),failures=0,records=records),indent=2)+'\n');print(f'{len(records)} explicit selected-source bounds checks PASS')
