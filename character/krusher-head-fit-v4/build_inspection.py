from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];C=R/'character/krusher-james-canonical-v7';OLD=R/'character/krusher-inspection-family-v3';P=R/'character/krusher-inspection-family-v4';P.mkdir(exist_ok=True)
index=json.loads((R/'character/krusher-animation-package-v3/package.json').read_text());mapping={};checks=0;records=[]
for gear in ['bare','helmet']:
 m=json.loads((C/(gear+'-manifest.json')).read_text())
 for state in m['states']:
  previous=index['states'][gear+':'+state['id']]['sourceFrames']
  for old,new in zip(previous,state['frameFiles']):
   target='res://character/krusher-james-canonical-v7/'+new
   if (gear,old) in mapping:assert (R/mapping[gear,old][6:]).read_bytes()==(R/target[6:]).read_bytes()
   mapping[gear,old]=target
 m=json.loads((OLD/(gear+'-manifest.json')).read_text())
 for state in m['states']:
  files=[]
  for i,source in enumerate(state['frameFiles']):
   old=source[6:] if source.startswith('res://') else (OLD/source).resolve().relative_to(R).as_posix();target=mapping[gear,old];files.append(target);checks+=1;records.append({'gear':gear,'state':state['id'],'index':i,'source':source,'output':target,'outputHash':hashlib.sha256((R/target[6:]).read_bytes()).hexdigest()})
  state['frameFiles']=files
 (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
(P/'revision.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'scope':'Inspection aliases resolve to exact corrected canonical frames; original metadata preserved.'},indent=2)+'\n')
print(json.dumps({'inspectionReferences':checks,'errors':0}))
