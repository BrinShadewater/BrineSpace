from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((P/'verification.json').read_text());checks=0;errors=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for key,hkey in [('sourceManifest','sourceManifestHash'),('headSource','headHash')]:
 checks+=1
 if sha(R/v[key])!=v[hkey]:errors.append(key)
source=json.loads((R/v['sourceManifest']).read_text());out=json.loads((P/'manifest.json').read_text())
for state in out['states']:
 original=next(t for t in source['states'] if t['id']==state['id'])
 for key,val in original.items():
  if key=='frameFiles':continue
  checks+=1
  if state.get(key)!=val:errors.append('metadata:'+state['id']+':'+key)
for t in v['records']:
 a=np.array(Image.open(R/t['source']).convert('RGBA'));b=np.array(Image.open(P/t['output']).convert('RGBA'));mask=np.array(Image.open(P/t['allowedMask']))>0
 checks+=4
 if sha(R/t['source'])!=t['sourceHash']:errors.append('source:'+t['output'])
 if sha(P/t['output'])!=t['outputHash']:errors.append('output:'+t['output'])
 if not np.array_equal(a[~mask],b[~mask]):errors.append('outside:'+t['output'])
 if not np.array_equal(a[:,:,3],b[:,:,3]):errors.append('alpha:'+t['output'])
report={'checks':checks,'errors':errors,'scope':'Source/output hashes, state metadata, source pixels outside face/marking masks and exact source alpha; source shell/visor geometry retained, no temporal acceptance'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not errors
