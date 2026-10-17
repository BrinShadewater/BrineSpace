from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];reg=json.loads((HERE/'registration.json').read_text());hashes=json.loads((HERE/'frame-hashes.json').read_text());checks=0;metrics={}
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
manifests={mode:json.loads((HERE/(mode+'-manifest.json')).read_text()) for mode in ['bare','helmet']}
for mode,m in manifests.items():
 check(m['pivot']==[128,224] and m['standingHeight']==148,'master profile');check(len(m['states'])==4,'coverage');metrics[mode]={}
 for st in m['states']:
  key=st['id'];rows=reg[mode][key];check(len(st['frameFiles'])==11 and st['frameCount']==11,'11 poses');check(sum(st['frameDurationsMs'])==1600 and st['frameDurationsMs'][5]==200 and not st['loop'],'merged seam timing');metrics[mode][key]=[]
  for i,f in enumerate(st['frameFiles']):
   p=HERE/f;im=Image.open(p).convert('RGBA');a=np.array(im);r=rows[i];check(a.shape==(256,256,4),'canvas');check(hashlib.sha256(p.read_bytes()).hexdigest()==hashes[f]==r['sha256'],'hash');check(im.tobytes()==Image.open(ROOT/r['source']).convert('RGBA').tobytes(),'unchanged donor pixels');check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any(),'unclipped')
   yy,xx=np.indices(a.shape[:2]);y,x=np.where(a[:,:,3]>180);metrics[mode][key].append(dict(crown=int(y.min()),sole=int(y.max()),height=int(y.max()-y.min()+1)));fy,fx=np.where((a[:,:,3]>180)&(yy>214));check(len(fx)>0 and fx.max()-fx.min()+1<=56 and 221<=fy.max()<=225,'compact planted feet')
   if mode=='bare':check(147<=y.max()-y.min()+1<=149 and 76<=y.min()<=77,'master sized body');b=np.array(Image.open(HERE/manifests['helmet']['states'][m['states'].index(st)]['frameFiles'][i]));check(np.array_equal(a[r['headCutoff']:],b[r['headCutoff']:]),'same body below neck')
 for fwd,rev in [('carry-turn-east-west','carry-turn-west-east'),('carry-turn-north-south','carry-turn-south-north')]:
  a=next(s for s in m['states'] if s['id']==fwd);b=next(s for s in m['states'] if s['id']==rev);check(a['frameDurationsMs']==b['frameDurationsMs'][::-1],'reverse timing')
  for i in range(11):check(Image.open(HERE/a['frameFiles'][i]).tobytes()==Image.open(HERE/b['frameFiles'][10-i]).tobytes(),'reverse pixels')
gif=Image.open(HERE/'review.gif');total=0
for i in range(gif.n_frames):gif.seek(i);total+=gif.info['duration']
check(total==8800,'decoded preview timing');gif.seek(3);gif.convert('RGB').save(HERE/'review-frame003.png')
report=dict(checks=checks,failures=0,states=4,references=88,runtimeMsPerHalfTurn=1600,exactDonorPixels=True,reverseExact=True,mergedSharedSeam=True,bodyBelowNeckExact=True,compactFeet=True,metrics=metrics,decodedGifMs=total,ownerReviewPending=True)
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Half turns:',checks,'checks,0 failures;88 exact donor references;decoded GIF8800ms')
