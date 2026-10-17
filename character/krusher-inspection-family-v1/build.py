"""Inspection aliases reuse the complete existing role action, with source clocks."""
from pathlib import Path
import copy,hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent;C=R/'character/krusher-james-canonical-v4';inventory=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text());checks=0;records=[]
for gear in ['bare','helmet']:
 cm=json.loads((C/(gear+'-manifest.json')).read_text());result={k:copy.deepcopy(v) for k,v in cm.items() if k!='states'};result.update(name='Krusher Dom '+gear+' inspection',status='candidate-not-installed',states=[])
 for direction in ['south','east','north','west']:
  key='inspect-'+direction;resolved=inventory['resolved'][gear][key];original=resolved['state'];role=next(s for s in cm['states'] if s['id']=='interact-'+direction)
  assert len(original['frameFiles'])==len(role['frameFiles']);checks+=1
  state=copy.deepcopy(original);state['frameFiles']=['res://'+(C/f).relative_to(R).as_posix() for f in role['frameFiles']];state['provenance']={'reuse':'Complete canonical-v4 Krusher role poses as inspection, same source frame count and chronology','timing':'Original selected inspection holds retained:6000ms instead of role action5500ms','loop':'Original inspection loop policy retained; exact canonical idle endpoints make loop joins identical'};result['states'].append(state)
  for f in state['frameFiles']:
   q=R/f.removeprefix('res://');records.append({'gear':gear,'state':key,'file':f,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
 (P/(gear+'-manifest.json')).write_text(json.dumps(result,indent=2)+'\n')
(P/'provenance.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'scope':'Inspection semantics reuse existing complete tablet action; original inspection timing and loop metadata retained, no new art.'},indent=2)+'\n');print(json.dumps({'states':8,'references':len(records),'checks':checks,'errors':[]}))
