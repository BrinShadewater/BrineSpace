from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];checks=0
hashes=json.loads((HERE/'frame-hashes.json').read_text())
for mode in ['bare','helmet']:
 m=json.loads((HERE/(mode+'-manifest.json')).read_text());rows={}
 for st in m['states']:
  assert len(st['frameFiles'])==6 and sum(st['frameDurationsMs'])==(840 if st['id']=='carry-east' else 520);checks+=2
  assert st['loop']==(st['id']=='carry-east');checks+=1;rows[st['id']]=[]
  for f in st['frameFiles']:
   im=Image.open(HERE/f).convert('RGBA');a=np.array(im);assert a.shape==(256,256,4);checks+=1
   assert not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any();checks+=1
   assert hashlib.sha256((HERE/f).read_bytes()).hexdigest()==hashes[f];checks+=1;rows[st['id']].append(a)
 for i in range(6):assert np.array_equal(rows['pickup-east'][i],rows['unload-east'][5-i]);checks+=1
 assert len({x[150:240].tobytes() for x in rows['carry-east']})==6;checks+=1
 folder=ROOT/('character/crew-runtime-matte-v1/branforth' if mode=='bare' else 'character/james-shared-helmet-runtime-v1');idle=json.loads((folder/'manifest.json').read_text());st=next(s for s in idle['states'] if s['id']=='idle-east');out=Image.new('RGBA',(256,256));out.alpha_composite(Image.open(folder/st['frameFiles'][0]).convert('RGBA'),(36,52));a=np.array(out);mask=np.ones((256,256),bool);mask[190:225,155:230]=False
 assert np.array_equal(a[mask],rows['pickup-east'][0][mask]);checks+=1
report={'checks':checks,'failures':0,'frames':36,'lowerBodyCarryPoses':6,'fixedScale':json.loads((HERE/'registration.json').read_text())['fixedScale'],'unload':'Exact reversed pickup','endpoint':'Exact selected actor idle pixels outside deposited case','staged':False};(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
