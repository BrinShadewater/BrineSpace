from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((P/'verification.json').read_text());checks=0;errors=[]
for t in v['records']:
 for key,hkey,root in [('source','sourceHash',R),('headSource','headHash',R),('output','outputHash',P)]:
  checks+=1
  if hashlib.sha256((root/t[key]).read_bytes()).hexdigest()!=t[hkey]:errors.append(t[key])
 if t['family']=='bill':continue
 source=np.array(Image.open(R/t['source']).convert('RGBA'));output=np.array(Image.open(P/t['output']).convert('RGBA'))
 mask=np.array(Image.open(P/f"masks/{t['family']}-{t['direction']}-allowed.png"))>0
 collar=np.array(Image.open(P/f"masks/{t['family']}-{t['direction']}-collar.png"))>0
 checks+=2
 if not np.array_equal(source[~mask],output[~mask]):errors.append('protected:'+t['output'])
 if not np.array_equal(source[collar],output[collar]):errors.append('collar:'+t['output'])
report={'checks':checks,'errors':errors,'scope':'Frozen source/head/output hashes and protected source body/collar pixels; no animation or semantic-mask acceptance'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));assert not errors
