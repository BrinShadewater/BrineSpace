from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from build import mask,GAINS
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];reg=json.loads((HERE/'registration.json').read_text());hashes=json.loads((HERE/'frame-hashes.json').read_text());checks=0;changed=0
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
for mode in ['bare','helmet']:
 m=json.loads((HERE/(mode+'-manifest.json')).read_text());check(len(m['states'])==12,'coverage');check(m['pivot']==[128,224] and m['standingHeight']==148,'profile')
 for st in m['states']:
  d=st['id'].split('-')[-1];rows=reg[mode][st['id']];check(len(st['frameFiles'])==len(rows)==(7 if st['id']=='unload-north' else 6),'poses');check(sum(st['frameDurationsMs'])==(840 if st['id'].startswith('carry-') else 520),'timing')
  for i,f in enumerate(st['frameFiles']):
   a=np.array(Image.open(HERE/f).convert('RGBA'));r=rows[i];src=ROOT/r['source'];old=np.array(Image.open(src).convert('RGBA'));gold=mask(Image.open(ROOT/r['bareMaskSource']).convert('RGBA'))
   if r['protectedMasterEndpoint']:gold[:]=False
   check(a.shape==(256,256,4),'canvas');check(hashlib.sha256(src.read_bytes()).hexdigest()==r['sourceSha256'],'original source unchanged');check(hashlib.sha256((HERE/f).read_bytes()).hexdigest()==hashes[f]==r['sha256'],'hash');check(np.array_equal(a[:,:,3],old[:,:,3]),'exact alpha');check(np.array_equal(a[~gold],old[~gold]),'exact non-gold/head/cloth');check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any(),'unclipped')
   if r['protectedMasterEndpoint'] or d=='north':check(np.array_equal(a,old),'protected exact frame')
   changed+=int(not np.array_equal(a,old))
 for d in GAINS:
  p=next(s for s in m['states'] if s['id']=='pickup-'+d);u=next(s for s in m['states'] if s['id']=='unload-'+d)
  indices=[5,4,3,2,1,3,0] if d=='north' else [5,4,3,2,1,0]
  for i,source in enumerate(indices):check(Image.open(HERE/p['frameFiles'][source]).tobytes()==Image.open(HERE/u['frameFiles'][i]).tobytes(),'exact selected action pose reuse')
gif=Image.open(HERE/'review.gif');total=0
for i in range(gif.n_frames):gif.seek(i);total+=gif.info['duration']
check(total==10880,'decoded duration');gif.seek(7);gif.convert('RGB').save(HERE/'review-frame007.png')
report=dict(checks=checks,failures=0,frameReferences=146,changedReferences=changed,allAlphaExact=True,allOutsideGoldExact=True,northExact=True,groundEndpointsExact=True,sourcePoseReuseExact=True,decodedGifMs=total,legacyGifDoesNotShowNewNorthTiming=True,ownerReviewPending=True);(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
