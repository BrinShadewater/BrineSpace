from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];OLD=R/'character/krusher-animation-package-v2'
read=lambda p:json.loads(p.read_text());index=read(P/'package.json');before=read(OLD/'package.json');revision=read(P/'palette-revision.json');changed={q['source']:q for q in revision['records']};checks=0;errors=[];slots=0
def check(ok,name):
 global checks
 checks+=1
 if not ok:errors.append(name)
check(set(index['states'])==set(before['states']),'whole state coverage')
for key,q in index['states'].items():
 old=before['states'][key];a=read(OLD/old['manifest']);b=read(P/q['manifest']);sa=next(s for s in a['states'] if s['id']==key.split(':',1)[1]);sb=next(s for s in b['states'] if s['id']==sa['id'])
 check({k:v for k,v in a.items() if k!='states'}=={k:v for k,v in b.items() if k!='states'},key+' whole render profile')
 check({k:v for k,v in sa.items() if k!='frameFiles'}=={k:v for k,v in sb.items() if k!='frameFiles'},key+' whole source choreography')
 check(len(sa['frameFiles'])==len(sb['frameFiles']),key+' complete frames')
 for x,y in zip(sa['frameFiles'],sb['frameFiles']):
  src=(OLD/old['manifest']).parent/x;dst=(P/q['manifest']).parent/y;rel=src.resolve().relative_to(OLD.resolve()).as_posix();aa=np.array(Image.open(src).convert('RGBA'));bb=np.array(Image.open(dst).convert('RGBA'));rec=changed.get(rel)
  mask=np.array(Image.open(P/rec['mask']))>0 if rec else np.zeros(aa.shape[:2],bool)
  check(dst.resolve().is_relative_to(P.resolve()),key+' portable path')
  check(np.array_equal(aa[~mask],bb[~mask]),key+' all non-shoulder pixels exact')
  check(np.array_equal(aa[:,:,3],bb[:,:,3]),key+' entire silhouette alpha exact')
  if rec:
   check(hashlib.sha256(src.read_bytes()).hexdigest()==rec['sourceHash'],key+' reviewed source hash')
   check(hashlib.sha256(dst.read_bytes()).hexdigest()==rec['outputHash'],key+' reviewed output hash')
   check(np.all(bb[mask,1]>=bb[mask,0]) and np.all(bb[mask,2]>=bb[mask,1]) and np.all(bb[mask,:3]<=177),key+' muted cyan matte patches')
  else:check(src.read_bytes()==dst.read_bytes(),key+' untouched PNG byte exact')
  slots+=1
result={'checks':checks,'errors':errors,'states':len(index['states']),'slots':slots,'recolouredFrames':len(changed),'scope':'Entire prior corrected library preserved except explicit reviewed shoulder masks; all profiles/clocks/metadata and every non-mask RGBA pixel exact. Native admission and station visual review separate.'};(P/'palette-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='scope'}));assert not errors
