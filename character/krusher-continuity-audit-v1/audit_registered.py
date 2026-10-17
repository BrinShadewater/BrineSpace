from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
H=Path('character/krusher-continuity-audit-v1');roots=[Path('character/krusher-animation-package-v9'),Path('character/krusher-animation-package-v10')];groups={};slots=0
for root in roots:
 p=json.loads((root/'package.json').read_text());cache={};signatures={}
 for key,q in p['states'].items():
  m=cache.setdefault(q['manifest'],json.loads((root/q['manifest']).read_text()));s=next(s for s in m['states'] if s['id']==key.split(':',1)[1])
  for i,f in enumerate(s['frameFiles']):
   path=(root/q['manifest']).parent/f;sk=(str(path),tuple(m['pivot']))
   if sk not in signatures:
    im=Image.open(path).convert('RGBA');bb=im.getbbox();arr=np.array(im.crop(bb));arr[arr[:,:,3]==0]=0;sig=hashlib.sha256(arr.tobytes()+str((arr.shape,bb[0]-m['pivot'][0],bb[1]-m['pivot'][1])).encode()).hexdigest();signatures[sk]=sig
   if root==roots[0]:groups[(key,i)]=signatures[sk]
   else:groups[(key,i)]=(groups[(key,i)],signatures[sk])
by={}
for slot,(old,new) in groups.items():by.setdefault(old,{}).setdefault(new,[]).append(slot)
conflicts=[v for v in by.values() if len(v)>1];report={'slots':len(groups),'registeredPoseGroups':len(by),'conflicts':conflicts};(H/'registered-alias-audit.json').write_text(json.dumps(report,indent=2));print({'slots':len(groups),'registeredPoseGroups':len(by),'conflicts':len(conflicts)})
