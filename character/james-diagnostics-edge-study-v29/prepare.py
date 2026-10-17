from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
inventory=r/'character/james-full-set-review-2026-10-02/current-selection-v27/source-inventory.json';d=json.loads(inventory.read_bytes());records=[];files=[inventory,Path(__file__),p/'edge-study.gd',p/'edge-material.gdshader',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
for direction,indices in [('south',[35,70,122]),('north',[34,68,119]),('west',[38,76,134])]:
 for mode in ['bare','helmet']:
  state=d['states'][mode]['inspect-'+direction];master=d['states'][mode]['idle-'+direction];f=r/master['frameFiles'][0];files.append(f)
  for i in indices:
   source=r/state['frameFiles'][i];files.append(source);records.append(dict(direction=direction,mode=mode,slot=i,source='res://'+state['frameFiles'][i],master='res://'+master['frameFiles'][0],pivot=state['pivot'],standingHeight=state['standingHeight']))
(p/'source-contract.json').write_text(json.dumps(dict(records=records),indent=2)+'\n');files.append(p/'source-contract.json')
(p/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)}),indent=2)+'\n')
print('18 representative paired poses frozen for edge-only native material study.')
