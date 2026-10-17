from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;inventory=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text());proof=json.loads((P/'provenance.json').read_text());checks=0;errors=[]
def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
for r in proof['records']:check(hashlib.sha256((R/r['file'].removeprefix('res://')).read_bytes()).hexdigest()==r['sha256'],'frozen canonical hash')
for gear in ['bare','helmet']:
 m=json.loads((P/(gear+'-manifest.json')).read_text());cm=json.loads((R/'character/krusher-james-canonical-v4'/(gear+'-manifest.json')).read_text())
 for s in m['states']:
  resolved=inventory['resolved'][gear][s['id']];old=resolved['state'];mp=R/resolved['manifest'].removeprefix('res://');check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in old.items() if k not in ['frameFiles','provenance']},'inspection metadata')
  for i,f in enumerate(s['frameFiles']):
   out=np.array(Image.open(R/f.removeprefix('res://')).convert('RGBA'));src=old['frameFiles'][i];q=R/src.removeprefix('res://') if src.startswith('res://') else mp.parent/src;source=np.array(Image.open(q).convert('RGBA'))
   yy,xx=np.indices(source.shape[:2]);rgb=source[:,:,:3].astype(float);target=np.array([82.,124.,128.]);luma=np.array([.2126,.7152,.0722]);gain=np.minimum(1.15,(rgb@luma)/(target@luma));cyan=np.rint(gain[:,:,None]*target).astype('uint8')
   yellow=(rgb[:,:,0]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65)
   department=yellow&(yy>=90)&(yy<110)&np.all(out[:,:,:3]==cyan,axis=2)&(out[:,:,3]==source[:,:,3])
   changed=np.any(source!=out,axis=2)&(yy>=90);check(not np.any(changed&(~department)),'source lower suit/tool pose order except exact cyan marking')
  first=np.array(Image.open(R/s['frameFiles'][0].removeprefix('res://')).convert('RGBA'));last=np.array(Image.open(R/s['frameFiles'][-1].removeprefix('res://')).convert('RGBA'));check(np.array_equal(first,last),'exact loop closure')
  idle=next(row for row in cm['states'] if row['id']=='idle-'+s['id'].rsplit('-',1)[1]);check(np.array_equal(first,np.array(Image.open(R/'character/krusher-james-canonical-v4'/idle['frameFiles'][0]).convert('RGBA'))),'exact canonical idle')
result={'checks':checks,'errors':errors,'scope':'All1146frozen canonical inputs, source lower suit/tool pose correspondence, original inspection metadata and complete RGBA loop/idle joins'};(P/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not errors
