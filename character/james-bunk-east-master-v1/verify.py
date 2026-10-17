from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;checks=0
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
bare=json.loads((HERE/'bare-manifest.json').read_text());helmet=json.loads((HERE/'helmet-manifest.json').read_text());reg=json.loads((HERE/'registration.json').read_text());heads=json.loads((HERE/'helmet-registration.json').read_text())
for mode,pack in [('bare',bare),('helmet',helmet)]:
 for st in pack['states']:
  check(sum(st['frameDurationsMs'])==1840 if st['id']!='bunk-sleep-east' else True,'controller timing')
  for i,f in enumerate(st['frameFiles']):
   a=np.array(Image.open(HERE/f).convert('RGBA'));check(a.shape==(256,256,4),'canvas');check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any(),'clearance');idx=st['provenance']['sourcePoses'][i]
   if idx!=0:
    b=np.array(Image.open(HERE/'registered-ungraded'/f'{idx:03d}.png').convert('RGBA'))
    if mode=='bare':
     check(np.array_equal(a[:,:,3],b[:,:,3]),'grade preserves alpha');x0,y0,x1,y1=reg['tracking'][idx]['protectedHeadBox'];check(np.array_equal(a[y0:y1,x0:x1],b[y0:y1,x0:x1]),'face/hair protected')
    else:
     bs=next(s for s in bare['states'] if s['id']==st['id']);body=np.array(Image.open(HERE/bs['frameFiles'][i]).convert('RGBA'));x0,y0,x1,y1=heads['tracking'][idx]['editRegion'];mask=np.ones(a.shape[:2],bool);mask[y0:y1,x0:x1]=False;check(np.array_equal(a[mask],body[mask]),'body outside head exact');check(heads['tracking'][idx]['fixedHeadScale']==reg['fixedScale'],'one helmet scale')
 for idx in range(7):
  enter=next(s for s in pack['states'] if s['id']=='bunk-enter-east');exit=next(s for s in pack['states'] if s['id']=='bunk-exit-east');check(Image.open(HERE/enter['frameFiles'][idx]).tobytes()==Image.open(HERE/exit['frameFiles'][6-idx]).tobytes(),'exact reverse')
 sleep=next(s for s in pack['states'] if s['id']=='bunk-sleep-east');check(Image.open(HERE/sleep['frameFiles'][0]).tobytes()==Image.open(HERE/enter['frameFiles'][-1]).tobytes(),'shared sleep seam')
for bs,hs in zip(bare['states'],helmet['states']):
 for field in ['id','frameDurationsMs','loop','furnitureFrames','depthOffsets']:check(bs[field]==hs[field],'paired furniture '+field)
(HERE/'validation.json').write_text(json.dumps(dict(checks=checks,failures=0,bareReferences=15,helmetReferences=15,fixedScale=reg['fixedScale'],masterHeight=148,ownerReviewPending=True),indent=2)+'\n');print(checks,'checks,0 failures')
