from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from build import endpoint
HERE=Path(__file__).resolve().parent;hashes=json.loads((HERE/'frame-hashes.json').read_text());reg=json.loads((HERE/'registration.json').read_text());checks=0
for mode in ['bare','helmet']:
 m=json.loads((HERE/(mode+'-manifest.json')).read_text());states={s['id']:s for s in m['states']};assert len(states)==2;checks+=1
 for st in states.values():
  assert len(st['frameFiles'])==6 and sum(st['frameDurationsMs'])==800 and not st['loop'];checks+=1
  for f in st['frameFiles']:
   a=np.array(Image.open(HERE/f));assert a.shape==(256,256,4);checks+=1;assert not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any();checks+=1;assert hashlib.sha256((HERE/f).read_bytes()).hexdigest()==hashes[f];checks+=1
 forward=states['carry-turn-east-south']['frameFiles'];reverse=states['carry-turn-south-east']['frameFiles']
 for i in range(6):assert Image.open(HERE/forward[i]).tobytes()==Image.open(HERE/reverse[5-i]).tobytes();checks+=1
 for i,d in [(0,'east'),(5,'south')]:
  a=np.array(Image.open(HERE/forward[i]));cutoff=reg['tracking'][i]['legCutoff'];assert np.array_equal(a[:cutoff],np.array(endpoint(d,mode))[:cutoff]);checks+=1
 for i in range(6):
  a=np.array(Image.open(HERE/forward[i]));old=np.array(Image.open(HERE/'before-planted-v2'/forward[i]));cutoff=reg['tracking'][i]['legCutoff'];assert np.array_equal(a[:cutoff],old[:cutoff]);checks+=1
  y,x=np.where((a[:,:,3]>180)&(np.indices(a.shape[:2])[0]>214));assert len(x)>0 and x.max()-x.min()+1<=55 and 221<=y.max()<=225;checks+=1
for i in range(1,5):
 a=np.array(Image.open(HERE/('frames/bare/carry-turn-east-south/%03d.png'%i)));b=np.array(Image.open(HERE/('frames/helmet/carry-turn-east-south/%03d.png'%i)));cutoff=reg['tracking'][i]['headCutoff'];assert np.array_equal(a[cutoff:],b[cutoff:]);checks+=1
im=Image.open(HERE/'review-planted-v2.gif');total=0
for i in range(im.n_frames):im.seek(i);total+=im.info['duration']
assert total==2800;checks+=1
report={'checks':checks,'failures':0,'references':24,'durationMsPerTurn':800,'exactAcceptedUpperBodyEndpoints':True,'reverseExact':True,'helmetBodyBelowCutoffExact':True,'decodedGifMs':total,'previewOnly':'300ms extra holds at each endpoint','staged':False};(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
