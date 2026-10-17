from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
v=json.loads((P/'verification.json').read_text());checks=0;errors=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for path,key in [('sourceManifest','sourceManifestHash'),('headSource','headSourceHash'),('canonicalIdle','canonicalIdleHash')]:
 checks+=1
 if sha(R/v[path])!=v[key]:errors.append(path)
original=json.loads((R/v['sourceManifest']).read_text());out=json.loads((P/'bare-manifest.json').read_text());s=out['states'][0];source=next(t for t in original['states'] if t['id']==s['id'])
for key,value in source.items():
 if key=='frameFiles':continue
 checks+=1
 if s[key]!=value:errors.append('metadata:'+key)
for t in v['records']:
 a=np.array(Image.open(R/t['source']).convert('RGBA'));b=np.array(Image.open(P/t['output']).convert('RGBA'));allowed=np.array(Image.open(P/t['mask']))>0
 checks+=4
 if sha(R/t['source'])!=t['sourceHash']:errors.append('source:'+t['output'])
 if sha(P/t['output'])!=t['outputHash']:errors.append('output:'+t['output'])
 if not np.array_equal(a[~allowed],b[~allowed]):errors.append('protected:'+t['output'])
 visible=np.array(Image.open(P/t['tabletMask']))>0
 if not np.array_equal(a[visible],b[visible]):errors.append('tablet:'+t['output'])
idle=np.array(Image.open(R/v['canonicalIdle']).convert('RGBA'))
for index in [0,-1]:
 checks+=1
 if not np.array_equal(np.array(Image.open(P/s['frameFiles'][index]).convert('RGBA')),idle):errors.append('canonical endpoint')
report={'checks':checks,'errors':errors,'scope':'Current source/output hashes, state metadata, protected body/tablet pixels and exact canonical idle endpoints; no temporal artistic acceptance'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));assert not errors
