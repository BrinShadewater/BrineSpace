from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((P/'verification.json').read_text());checks=0;errors=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks+=2
if sha(R/v['sourceManifest'])!=v['sourceManifestHash']:errors.append('sourceManifest')
if sha(R/'character/krusher-veld-motion-fit-v2/verification.json')!=v['fitVerificationHash']:errors.append('fitVerification')
source=json.loads((R/v['sourceManifest']).read_text());out=json.loads((P/'manifest.json').read_text())
for state in out['states']:
 original=next(t for t in source['states'] if t['id']==state['id'])
 for key,value in original.items():
  if key=='frameFiles':continue
  checks+=1
  if state.get(key)!=value:errors.append('metadata:'+state['id']+':'+key)
for t in v['records']:
 a=np.array(Image.open(R/t['source']).convert('RGBA'));b=np.array(Image.open(P/t['output']).convert('RGBA'));mask=np.array(Image.open(P/t['markingMask']))>0
 checks+=5
 if sha(R/t['source'])!=t['sourceHash']:errors.append('source:'+t['output'])
 if sha(P/t['output'])!=t['outputHash']:errors.append('output:'+t['output'])
 if not np.array_equal(a[~mask],b[~mask]):errors.append('outside:'+t['output'])
 if not np.array_equal(a[:,:,3],b[:,:,3]):errors.append('alpha:'+t['output'])
 if not np.array_equal(a[t['toolProtectionFromRow']:],b[t['toolProtectionFromRow']:]):errors.append('tools:'+t['output'])
report={'checks':checks,'errors':errors,'scope':'Input/output hashes, exact pixels outside marking mask, alpha, lower tools and source state metadata; not continuous motion acceptance'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not errors
