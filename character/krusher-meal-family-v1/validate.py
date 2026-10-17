from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
proof=json.loads((P/'provenance.json').read_text());checks=0;errors=[]
def check(ok,why):
 global checks
 checks+=1
 if not ok:errors.append(why)
for record in proof['records']:
 for path,hash_key in [('source','sourceHash'),('originalMealSource','originalSourceHash'),('headSource','headHash')]:check(hashlib.sha256((R/record[path]).read_bytes()).hexdigest()==record[hash_key],path+' hash')
 out=np.array(Image.open(P/record['output']).convert('RGBA'));check(out.shape==(256,256,4),'canvas');check(hashlib.sha256((P/record['output']).read_bytes()).hexdigest()==record['outputHash'],'output hash')
 if record['gear']=='bare':
  im=Image.open(R/record['source']).convert('RGBA');pad=Image.new('RGBA',(256,256));pad.alpha_composite(im,tuple(record['sourcePadding']));a=np.array(pad);allowed=np.array(Image.open(P/record['allowedMask']))>0;foreground=np.array(Image.open(P/record['foregroundMask']))>0
  check(np.array_equal(a[~allowed],out[~allowed]),'protected body');check(np.array_equal(a[foreground],out[foreground]),'hands/cup/spoon foreground');check(np.array_equal(a[141:],out[141:]),'lower utility suit and feet')
 else:
  pad=Image.new('RGBA',(256,256));pad.alpha_composite(Image.open(R/record['source']).convert('RGBA'),(36,52));check(np.array_equal(np.array(pad),out),'exact existing helmet pose')
for gear in ['bare','helmet']:
 m=json.loads((P/(gear+'-manifest.json')).read_text());check((m['pivot'],m['standingHeight'])==([128,224],148),'ruler');check(len(m['states'])==8,'cardinal actions')
 for s in m['states']:
  row=next(r for r in proof['records'] if r['gear']==gear and r['state']==s['id']);source=json.loads((R/row['sourceManifest'].removeprefix('res://')).read_text());original=next(t for t in source['states'] if t['id']==s['id']);check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in original.items() if k not in ['frameFiles','provenance']},'state timing/events/loop '+s['id'])
result={'checks':checks,'errors':errors,'scope':'All input/output hashes; exact padded source protection and hand/utensil masks; same state clocks/events/loop; exact sealed inspection poses'};(P/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not errors
