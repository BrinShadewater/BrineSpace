from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parent.parent
b=json.loads((P/'bindings.json').read_text(encoding='utf-8'));reg=json.loads((P/'registration.json').read_text(encoding='utf-8'));checks=0
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
for file,digest in b['sourceSha256'].items():check(hashlib.sha256((R/file).read_bytes()).hexdigest()==digest,'Frozen canonical source bytes')
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text(encoding='utf-8'));state=m['states'][0]
 check(m['status']=='staged_visual_review' and m['standingHeight']==148 and m['pivot']==[128,224],'Staged registration')
 check(not state['loop'] and sum(state['frameDurationsMs'])==320 and len(state['frameFiles'])==6,'Bounded320ms first step')
 held=Image.open(R/(b['held'] if gear=='bare' else 'character/bill-cargo-east-master-head-v1/frames/helmet/pickup-east/010.png')).convert('RGBA')
 for i,file in enumerate(state['frameFiles']):
  path=R/file.removeprefix('res://');im=Image.open(path).convert('RGBA');a=np.array(im)
  check(im.size==(256,256),'Canonical source canvas')
  y,x=np.where(a[:,:,3]>180);check(y.min()>0 and y.max()<=225 and x.min()>0 and x.max()<255,'Complete anatomy and foot extent')
  if i in [0,5]:
   source=R/(b['held'] if gear=='bare' else 'character/bill-cargo-east-master-head-v1/frames/helmet/pickup-east/010.png') if i==0 else R/(b['carry'] if gear=='bare' else b['helmetCarry'])['sourceFiles'][0].removeprefix('res://')
   check(path.read_bytes()==source.read_bytes(),'Exact held/walk endpoint bytes')
  else:
   rec=reg['frames'][i-1];dy=rec['upperTranslation'][1];expected=Image.new('RGBA',(256,256));expected.alpha_composite(held,(0,dy));e=np.array(expected);Y,X=np.indices(e.shape[:2]);mask=(Y<rec['seam'])|((X>=135)&(Y<170+dy))
   check(np.array_equal(a[mask],e[mask]),'Exact master upperbody/gear pixels at recorded rigid translation')
   check(rec['scale']==reg['calibration']['scale'],'One shared source ruler')
   labels,_=label(a[:,:,3]>180);counts=np.bincount(labels.ravel());counts[0]=0;check(counts.max()/counts.sum()>.98,'Connected fitted anatomy')
bare=[np.array(Image.open(P/f'frames/bare/carry-start-east/{i:03}.png')) for i in range(1,5)]
helmet=[np.array(Image.open(P/f'frames/helmet/carry-start-east/{i:03}.png')) for i in range(1,5)]
for a,h in zip(bare,helmet):check(np.array_equal(a[140:],h[140:]),'Paired lowerbody exact')
print(f'BILL EAST FIRST STEP: {checks} checks pass')
(P/'validation.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'Package/pixels/shared ruler/paired body/endpoints only; not full motion or native acceptance'},indent=2)+'\n',encoding='utf-8')
