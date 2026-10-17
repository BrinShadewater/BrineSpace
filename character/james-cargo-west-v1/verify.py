from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;hashes=json.loads((HERE/'frame-hashes.json').read_text());checks=0
for mode in ['bare','helmet']:
 m=json.loads((HERE/(mode+'-manifest.json')).read_text());states={s['id']:s for s in m['states']};assert set(states)=={'pickup-west','carry-west','unload-west'};checks+=1
 for key,st in states.items():
  assert len(st['frameFiles'])==6;checks+=1;assert st['loop']==(key=='carry-west') and sum(st['frameDurationsMs'])==(840 if st['loop'] else 520);checks+=1;legs=[]
  for f in st['frameFiles']:
   a=np.array(Image.open(HERE/f).convert('RGBA'));assert a.shape==(256,256,4);checks+=1;assert not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any();checks+=1;assert hashlib.sha256((HERE/f).read_bytes()).hexdigest()==hashes[f];checks+=1;legs.append(a[160:240].tobytes())
  if key=='carry-west':assert len(set(legs))==6;checks+=1
 def pixels(f):return Image.open(HERE/f).tobytes()
 p=states['pickup-west']['frameFiles'];u=states['unload-west']['frameFiles'];c=states['carry-west']['frameFiles']
 for i in range(6):assert pixels(p[i])==pixels(u[5-i]);checks+=1
 assert pixels(p[-1])==pixels(c[0])==pixels(u[0]);checks+=1
for f,h in json.loads((HERE/'accepted-carry-hashes.json').read_text()).items():assert hashlib.sha256((HERE/f).read_bytes()).hexdigest()==h;checks+=1
report={'checks':checks,'failures':0,'references':36,'carryPoses':6,'pickupUnloadMs':520,'carryDurationMs':840,'acceptedCarryUnchanged':True,'unload':'Exact reversed pickup','staged':False};(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
