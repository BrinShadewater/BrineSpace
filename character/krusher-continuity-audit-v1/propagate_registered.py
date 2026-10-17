from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path.cwd();H=R/'character/krusher-continuity-audit-v1';B=R/'character/krusher-continuity-bank-v1';P=R/'character/krusher-animation-package-v9';rev=json.loads((B/'revision.json').read_text());by={q['source']:q for q in rev['records']};p=json.loads((P/'package.json').read_text());conf=json.loads((H/'registered-alias-audit.json').read_text())['conflicts'];changes={}
for group in conf:
 rels=set()
 for slots in group.values():
  for key,i in slots:
   mp=P/p['states'][key]['manifest'];m=json.loads(mp.read_text());s=next(s for s in m['states'] if s['id']==key.split(':',1)[1]);rels.add((mp.parent/s['frameFiles'][i]).resolve().relative_to(P).as_posix())
 winner=max((by[r] for r in rels),key=lambda q:q['changedPixels']);wi=Image.open(B/winner['output']).convert('RGBA');wb=wi.getbbox();arr=np.array(wi.crop(wb))
 for rel in rels:
  q=by[rel]
  if q is winner:continue
  original=Image.open(P/rel).convert('RGBA');a=np.array(original);bb=original.getbbox();out=np.zeros_like(a);out[bb[1]:bb[3],bb[0]:bb[2]]=arr;mask=np.any(a!=out,2);digest=hashlib.sha256(out.tobytes()+str(out.shape).encode()).hexdigest();dest=B/'frames'/(digest+'.png');Image.fromarray(out).save(dest);mp=B/'edit-masks'/(Path(rel).stem+'.png');Image.fromarray(mask.astype('uint8')*255).save(mp);oldpath='res://'+(P/rel).relative_to(R).as_posix() if 'outputUnchanged' in q else 'res://'+(B/q['output']).relative_to(R).as_posix();newpath='res://'+dest.relative_to(R).as_posix();changes[oldpath]=newpath;q.pop('outputUnchanged',None);q.update(output=dest.relative_to(B).as_posix(),mask=mp.relative_to(B).as_posix(),changedPixels=int(mask.sum()),outputHash=hashlib.sha256(dest.read_bytes()).hexdigest(),mode='Shared registered pose accent correction propagated across padded aliases')
for mp in (B/'packs').glob('*.json'):
 m=json.loads(mp.read_text())
 for s in m['states']:s['frameFiles']=[changes.get(f,f) for f in s['frameFiles']]
 mp.write_text(json.dumps(m,indent=2)+'\n')
(B/'revision.json').write_text(json.dumps(rev,indent=2)+'\n');print({'additionalDrawings':len(changes)})
