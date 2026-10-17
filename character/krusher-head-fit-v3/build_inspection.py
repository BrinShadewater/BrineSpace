from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
R=Path.cwd();old=R/'character/krusher-inspection-family-v2';P=R/'character/krusher-inspection-family-v3';P.mkdir(exist_ok=True);mapping={};checks=0
for q in json.loads((R/'character/krusher-james-canonical-v6/revision.json').read_text())['records']:
 if q['alias']:continue
 a=np.array(Image.open(R/q['source'][6:]).convert('RGBA'));mapping[q['gear'],hashlib.sha256(a.tobytes()).hexdigest()]='res://character/krusher-james-canonical-v6/'+q['output']
records=[]
for gear in ['bare','helmet']:
 name=gear+'-manifest.json';m=json.loads((old/name).read_text())
 for s in m['states']:
  files=[]
  for i,f in enumerate(s['frameFiles']):
   source=R/f[6:] if f.startswith('res://') else old/f;a=np.array(Image.open(source).convert('RGBA'));target=mapping[gear,hashlib.sha256(a.tobytes()).hexdigest()];files.append(target);records.append({'gear':gear,'state':s['id'],'index':i,'source':'res://'+source.relative_to(R).as_posix(),'sourceHash':hashlib.sha256(source.read_bytes()).hexdigest(),'output':target});checks+=1
  s['frameFiles']=files
 (P/name).write_text(json.dumps(m,indent=2)+'\n')
(P/'revision.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'scope':'All inspection references resolved by exact prior complete RGBA identity to revised canonical output; original root/state metadata retained. No new source drawings.'},indent=2)+'\n');(P/'pack-index.json').write_text(json.dumps({'candidatePacks':{'bare':['res://character/krusher-inspection-family-v3/bare-manifest.json'],'helmet':['res://character/krusher-inspection-family-v3/helmet-manifest.json']}},indent=2)+'\n');(P/'native').mkdir(exist_ok=True);(P/'native/verify.gd').write_text((old/'native/verify.gd').read_text().replace(old.name,P.name))
print(json.dumps({'inspectionPoseReferences':checks,'newDrawings':0}))
