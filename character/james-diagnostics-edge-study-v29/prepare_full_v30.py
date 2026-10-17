from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-diagnostics-edge-matte-v30';out.mkdir(exist_ok=True)
inventory=r/'character/james-full-set-review-2026-10-02/current-selection-v27/source-inventory.json';data=json.loads(inventory.read_bytes());records=[];files=[inventory,Path(__file__),p/'edge-study.gd',p/'edge-material.gdshader',p/'package-review.json',r/'character/james-side-motion-review-2026-10-02/run_validation.py']
for direction in ['south','north','west']:
 for mode in ['bare','helmet']:
  state=data['states'][mode]['inspect-'+direction];master=data['states'][mode]['idle-'+direction];files.extend([r/master['frameFiles'][0],r/state['manifest']])
  for i,ref in enumerate(state['frameFiles']):
   files.append(r/ref);records.append(dict(direction=direction,mode=mode,slot=i,source='res://'+ref,master='res://'+master['frameFiles'][0],pivot=state['pivot'],standingHeight=state['standingHeight'],preserveEndpoint=i in [0,state['frameCount']-1]))
(out/'source-contract.json').write_text(json.dumps(dict(records=records),indent=2)+'\n')
code=(p/'edge-study.gd').read_text().replace('james-diagnostics-edge-study-v29','james-diagnostics-edge-matte-v30')
code=code.replace('if aa==0 or 10*gg<=13*rr','if row.preserveEndpoint or aa==0 or 10*gg<=13*rr')
code=code.replace('str(row.slot).pad_zeros(3)','str(int(row.slot)).pad_zeros(3)')
code=code.replace(';18sources',';864sources').replace('18 representative native green-channel material studies.','864 staged full-cycle native green-channel material sources.').replace('Not all864sources or runtime/room acceptance.','Master endpoints exact. Full source visual review and normal/runtime/room adoption pending.')
(out/'edge-study.gd').write_text(code,encoding='utf-8');(out/'edge-material.gdshader').write_bytes((p/'edge-material.gdshader').read_bytes())
files += [out/'source-contract.json',out/'edge-study.gd',out/'edge-material.gdshader']
(out/'inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},
    scope='Full864frame native edge candidate staging, preserve endpoints and original per-phase alpha/pose. No normal adoption; preserve later V26East override and legacy meal aliases.'),indent=2)+'\n')
print('Full864frame edge staging prepared; all endpoints exact and normal loader unchanged.')
