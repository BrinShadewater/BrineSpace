from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;BARE=R.parent/'bill-cargo-east-coherent-v1'
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
first=m['states'][0]['frameFiles'][0];last=m['states'][2]['frameFiles'][-1]
check((R/first).read_bytes()==(R/last).read_bytes())
check(len({(R/f).read_bytes() for f in m['states'][1]['frameFiles']})==6)
print(f'Equipped east cargo:{checks} checks pass;23 references;body pixels/timing/profile/hash/alpha/idle joins')
