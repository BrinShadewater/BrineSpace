from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
R=Path.cwd();P=R/'character/bill-east-interact-master-consistency-v1';a=json.loads((P/'native/corrected-source-audit.json').read_text());s=a['selected']['bare']['idle-east'];rows=[];groups={}
for n,file in enumerate(s['files']):
 p=R/file;im=Image.open(p).convert('RGBA');rgba=hashlib.sha256(im.tobytes()).hexdigest();groups.setdefault(rgba,[]).append(n);y,x=np.where(np.array(im)[:,:,3]>127);rows.append({'slot':n,'path':file,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rgbaSha256':rgba,'bounds':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],'durationMs':s['timing'][n]})
q={'scope':'Current closure-selected East idle source baseline for next master consistency repair; source-only, no new native run. Preserve full authored breathing, not static repeated candidate.', 'count':len(rows),'uniqueRGBA':len(groups),'timelineMs':sum(s['timing']),'pivot':s['pivot'],'standingHeight':s['standingHeight'],'loop':s['loop'],'groups':list(groups.values()),'rows':rows,'originalMasterPath':'character/crew-side-masters-v1/bill-side-master-01.png','originalMasterSha256':hashlib.sha256((R/'character/crew-side-masters-v1/bill-side-master-01.png').read_bytes()).hexdigest()}
(P/'native/idle-source-baseline.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps({k:q[k] for k in ['count','uniqueRGBA','timelineMs','pivot','standingHeight','loop']}))
