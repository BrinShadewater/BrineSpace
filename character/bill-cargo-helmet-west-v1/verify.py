from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
R=Path(__file__).resolve().parent;BARE=R.parent/'bill-cargo-west-coherent-v1'
m=json.loads((R/'manifest.json').read_text());b=json.loads((BARE/'manifest.json').read_text());h=json.loads((R/'frame-hashes.json').read_text());reg=json.loads((R/'helmet-registration.json').read_text());checks=0
def check(ok):
 global checks
 assert ok;checks+=1
check(m['pivot']==[128,224]);check(m['standingHeight']==148);check(m['equipment']=='diving-helmet')
for s,t in zip(m['states'],b['states']):
 for key in ['id','frameFiles','frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']:check(s[key]==t[key])
for item in reg['frames']:
 f=item['file'];a=np.array(Image.open(R/f));old=np.array(Image.open(BARE/f));y=item['protectedBodyFromY']
 check(a.shape==(256,256,4));check(np.array_equal(a[y:],old[y:]));check(hashlib.sha256((R/f).read_bytes()).hexdigest()==h[f]);check(a[:,:,3].max()>180)
 check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any())
 components,n=label(a[:,:,3]>180);counts=np.bincount(components.ravel());counts[0]=0;body=int(counts.argmax())
 by,bx=np.where(components==body);ay,ax=np.where(a[:,:,3]>180)
 check(int(by.min())<=int(ay.min())+1)
first=m['states'][0]['frameFiles'][0];last=m['states'][2]['frameFiles'][-1]
check((R/first).read_bytes()==(R/last).read_bytes())
check(len({(R/f).read_bytes() for f in m['states'][1]['frameFiles']})==6)
for p,u in zip(m['states'][0]['frameFiles'],reversed(m['states'][2]['frameFiles'])):check((R/p).read_bytes()==(R/u).read_bytes())
canonical=np.array(Image.open(R/'sources/canonical-head.png'))
authority=np.array(Image.open(R.parent/'bill-equipped-west-selected-v1/frames/interact-west/000.png').crop((110,72,150,112)))
check(np.array_equal(canonical[:,:,:3][canonical[:,:,3]>0],authority[:,:,:3][canonical[:,:,3]>0]))
check(hashlib.sha256((R/'sources/canonical-head.png').read_bytes()).hexdigest()==reg['canonicalHeadSha256'])
for record in reg['frames']:
 if record['state']!='carry-west':continue
 check(record['angleDegrees']==0)
 a=np.array(Image.open(R/record['file']));x,y=record['helmetPosition'];head=a[y+13:y+53,x+22:x+62]
 check(np.array_equal(head[:,:,:3][canonical[:,:,3]==255],canonical[:,:,:3][canonical[:,:,3]==255]))
print(f'Equipped west cargo:{checks} checks pass;30 references;body pixels/timing/profile/hash/alpha/idle joins')
