from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((P/'verification.json').read_text());checks=0;errors=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,key in [('baseManifest','baseManifestHash'),('headSource','headHash')]:
 checks+=1
 if sha(R/v[path])!=v[key]:errors.append(path)
base=json.loads((R/v['baseManifest']).read_text());out=json.loads((P/'manifest.json').read_text())
for s in out['states']:
 original=next(t for t in base['states'] if t['id']==s['id'])
 for k,val in original.items():
  if k=='frameFiles':continue
  checks+=1
  if s.get(k)!=val:errors.append('metadata:'+s['id']+':'+k)
for t in v['records']:
 original=np.array(Image.open(R/t['source']).convert('RGBA'));candidate=np.array(Image.open(P/t['output']).convert('RGBA'));mask=np.array(Image.open(P/t['mask']))>0
 checks+=3
 if sha(R/t['source'])!=t['sourceHash']:errors.append('source:'+t['source'])
 if sha(P/t['output'])!=t['outputHash']:errors.append('output:'+t['output'])
 if not np.array_equal(original[~mask],candidate[~mask]):errors.append('protected:'+t['output'])
report={'checks':checks,'errors':errors,'scope':'Source/output fidelity, protected body/collar pixels and unchanged state metadata; not temporal artistic acceptance'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not errors
