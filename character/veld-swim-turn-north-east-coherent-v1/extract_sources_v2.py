from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent
source=H/'bare-source-v2.png';a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:4];assert len(ids)==4;ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/2)),np.where(lab==k)[1].mean()));records=[]
for i,k in enumerate(ids):
 y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert min(box[:2])>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0];cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;im=Image.fromarray(cut).crop(box);(H/'source-crops-v2').mkdir(exist_ok=True);im.save(H/f'source-crops-v2/{i:03}.png');records.append({'slot':i,'sourceBox':box,'size':list(im.size)})
(H/'source-extraction-v2.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'records':records,'checks':4,'failures':0,'status':'four connected source crops; fixed scale/grade and anatomical ownership review pending'},indent=2)+'\n');print('4 extracted source component bounds PASS')
