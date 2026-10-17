from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;hashes=json.loads((HERE/'frame-hashes.json').read_text());checks=0
for mode in ['bare','helmet']:
 m=json.loads((HERE/(mode+'-manifest.json')).read_text());states={s['id']:s for s in m['states']};assert set(states)=={'pickup-north','carry-north','unload-north'};checks+=1
 for key,st in states.items():
  assert len(st['frameFiles'])==st['frameCount']==(7 if key=='unload-north' else 6);checks+=1;assert st['loop']==(key=='carry-north') and sum(st['frameDurationsMs'])==(840 if st['loop'] else 520);checks+=1;legs=[]
  for f in st['frameFiles']:
   a=np.array(Image.open(HERE/f).convert('RGBA'));assert a.shape==(256,256,4);checks+=1;assert not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any();checks+=1;assert hashlib.sha256((HERE/f).read_bytes()).hexdigest()==hashes[f];checks+=1;legs.append(a[160:240].tobytes())
  if key=='carry-north':assert len(set(legs))==6;checks+=1
 def pixels(f):return Image.open(HERE/f).tobytes()
 p=states['pickup-north']['frameFiles'];u=states['unload-north']['frameFiles'];c=states['carry-north']['frameFiles']
 for i,source_index in enumerate([5,4,3,2,1,3,0]):assert pixels(p[source_index])==pixels(u[i]);checks+=1
 assert states['unload-north']['frameDurationsMs']==[80,100,100,90,40,40,70];checks+=1
 assert pixels(p[-1])==pixels(c[0])==pixels(u[0]);checks+=1
for f,h in json.loads((HERE/'accepted-carry-hashes.json').read_text()).items():assert hashlib.sha256((HERE/f).read_bytes()).hexdigest()==h;checks+=1
report={'checks':checks,'failures':0,'references':38,'carryPoses':6,'pickupUnloadMs':520,'carryDurationMs':840,'acceptedCarryUnchanged':True,'unload':'Reversed pickup with existing mid-rise reused before standing','staged':False};(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
