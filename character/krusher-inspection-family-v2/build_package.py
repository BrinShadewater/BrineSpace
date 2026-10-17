from pathlib import Path
import json,hashlib,shutil,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;old=R/'character/krusher-inspection-family-v1';canon=R/'character/krusher-james-canonical-v5'
index={};records=json.load(open(canon/'provenance.json'))['records'];unique={q['output']:q for q in records if not q.get('alias')}
for q in records:
 raw=hashlib.sha256(Image.open(R/q['source']).convert('RGBA').tobytes()).hexdigest();index[(q['gear'],raw)]=(canon/q['output'],canon/unique[q['output']]['mask'])
checks=0;rows=[];missing=[]
for gear in ['bare','helmet']:
 m=json.load(open(old/(gear+'-manifest.json')))
 for state in m['states']:
  files=[]
  for i,rel in enumerate(state['frameFiles']):
   src=R/rel[6:] if rel.startswith('res://') else old/rel;im=Image.open(src).convert('RGBA');raw=hashlib.sha256(im.tobytes()).hexdigest()
   if (gear,raw) not in index:missing.append([gear,state['id'],i]);continue
   revised,mask=index[(gear,raw)];a=np.array(im);b=np.array(Image.open(revised).convert('RGBA'));allowed=np.array(Image.open(mask))>0;assert np.array_equal(a[~allowed],b[~allowed]);checks+=1
   target=f'frames/{gear}/{state["id"]}/{i:03}.png';dst=P/target;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(revised,dst);files.append(target);rows.append({'gear':gear,'state':state['id'],'index':i,'source':src.relative_to(R).as_posix(),'newSource':revised.relative_to(R).as_posix(),'mask':mask.relative_to(R).as_posix(),'output':target})
  state['frameFiles']=files
 (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'revision.json').write_text(json.dumps({'checks':checks,'errors':missing,'records':rows,'scope':'Every original inspection frame binds exact old canonical RGBA and inherits corrected canonical drawing, with outside-head mask pixels exact and whole root/state metadata retained.'},indent=2)+'\n');print({'checks':checks,'missing':len(missing),'firstMissing':missing[:5]});assert not missing
