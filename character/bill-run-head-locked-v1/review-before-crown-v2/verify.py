from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1];m=json.loads((P/'manifest.json').read_text());hm=json.loads((P/'helmet-manifest.json').read_text());reg=json.loads((P/'head-registration.json').read_text());checks=[];hashes={};y,x=np.indices((256,256))
def check(ok,name):
 assert ok,name
 checks.append(name)
check(m['pivot']==[128,224] and m['standingHeight']==148,'Native master density')
for d in reg['directions']:
 direction=d['direction'];key='run-'+direction;s=next(s for s in m['states'] if s['id']==key);original=json.loads((P.parent/f'bill-run-{direction}-coherent-v1/manifest.json').read_text());gear=json.loads((P.parent/f'bill-run-{direction}-coherent-v1/helmet-manifest.json').read_text());hs=next(s for s in hm['states'] if s['id']==key)
 check(s['frameDurationsMs']==original['states'][0]['frameDurationsMs'] and s['loop']==original['states'][0]['loop'],'Original gait timing preserved')
 check(hs==gear['states'][0],'Equipment references/timing exactly preserved')
 check(m['strideDistanceCells'][key]==original['strideDistanceCells'][key],'Original directional stride preserved')
 head=np.array(Image.open(P/d['componentFile']).convert('RGBA'));master=np.array(Image.open(R/d['master']).convert('RGBA'));x0,y0,x1,y1=d['sourceBox'];mask=head[:,:,3]>0;check(np.array_equal(head[mask],master[y0:y1,x0:x1][mask]),'Master head pixels and alpha exact')
 for f,row in zip(s['frameFiles'],d['frames']):
  old=np.array(Image.open(R/row['originalFile'][6:]).convert('RGBA'));a=np.array(Image.open(R/f[6:]).convert('RGBA'));erase=np.array(Image.open(P/row['eraseMask']))>0;px,py=row['headPosition'];w,h=row['componentSize'];region=erase|((x>=px)&(x<px+w)&(y>=py)&(y<py+h))
  check(np.array_equal(a[~region],old[~region]),'Exact source body outside bounded head')
  opaque=head[:,:,3]==255;check(np.array_equal(a[py:py+h,px:px+w][opaque],head[opaque]),'Native head stamp exact')
  l,_=label(a[:,:,3]>160);sizes=np.bincount(l.ravel());check(sum(n>30 for n in sizes[1:])==1,'Head physically connected to body')
  check(row['nativeScale']==1 and a.shape==(256,256,4),'No anatomical rescale')
  check(hashlib.sha256((R/row['originalFile'][6:]).read_bytes()).hexdigest()==row['originalSha256'],'Original authored source unchanged');hashes[f]=hashlib.sha256((R/f[6:]).read_bytes()).hexdigest()
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'sha256':hashes,'scope':'Exact native head/body/unchanged equipped references/gait clocks and connected alpha; identity, collar fit and full motion require visual review'},indent=2)+'\n');print(str(len(checks))+' head/body/package checks pass')
