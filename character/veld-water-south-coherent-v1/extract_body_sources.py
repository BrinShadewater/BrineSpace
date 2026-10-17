from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;records=[];checks=0
for kind in ['tread','swim']:
 source=H/f'{kind}-source-v1.png';a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);counts=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:counts[k],reverse=True)[:6];assert len(ids)==6;checks+=1
 ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/2)),np.where(lab==k)[1].mean()))
 for i,k in enumerate(ids):
  y,x=np.where(lab==k);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];assert box[0]>0 and box[1]>0 and box[2]<a.shape[1] and box[3]<a.shape[0];checks+=1
  cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;cropBox=[box[0]-2,box[1]-2,box[2]+2,box[3]+2];im=Image.fromarray(cut).crop(cropBox);path=f'source-crops/{kind}/{i:03}.png';(H/path).parent.mkdir(parents=True,exist_ok=True);im.save(H/path);records.append({'kind':kind,'slot':i,'sourceBox':box,'paddedCropBox':cropBox,'projectedSourceSilhouette':[box[2]-box[0],box[3]-box[1]],'file':path,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest()})
(H/'body-source-inventory.json').write_text(json.dumps({'checks':checks,'failures':0,'rawBodyPoses':12,'installed':False,'status':'dense_source_crops_pending_fixed_scale_landmarks_palette_and_motion_fit','records':records},indent=2)+'\n',encoding='utf-8');print(f'{checks} raw body count/source-bound checks PASS;12 padded dense source crops saved.')
