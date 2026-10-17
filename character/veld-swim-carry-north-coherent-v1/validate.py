from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];checks=0
def check(ok):
 global checks
 checks+=1;assert ok,checks
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((R/'character/veld-water-cargo-master-audit-v1/current-selection.json').read_text())
fit=json.loads((H/'fit-checks.json').read_text());hashes={}
for gear in ['bare','helmet']:
 m=json.loads((H/f'{gear}-manifest.json').read_text());s=m['states'][0];old=baseline['records'][gear+'/north']['state']
 for field in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']:check(s[field]==old[field])
 check(m['frameWidth']==m['frameHeight']==256 and m['pivot']==[128,128] and m['standingHeight']==148 and m['precomposed'])
 check(len(s['frameFiles'])==6);check(sum(s['frameDurationsMs'])==840)
 for i,f in enumerate(s['frameFiles']):
  p=H/f;im=Image.open(p);a=np.array(im);check(im.mode=='RGBA' and im.size==(256,256));check(a[:,:,3].max()==255)
  check(not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20));hashes[f]=sha(p)
  check(fit['records'][i]['fixedAtlasScale']==fit['fixedAtlasScale'])
 check(len({hashes[f] for f in s['frameFiles']})==6)
check(fit['sourceSha256']==sha(H/'source-v3.png'))
check(fit['referenceSha256']==sha(R/fit['reference']))
native=json.loads((H/'native-candidate-v1-checks.json').read_text())
check(native['frameHashes']==hashes);check(native['failures']==0 and native['real_profile_changed_files']==[] and native['engine_errors']==[])
(H/'packaging-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,frameHashes=hashes,scope='Original clocks, profile, flags, six unique poses, alpha borders, fixed anatomical ruler, exact current native evidence; not world-route or full-set acceptance'),indent=2)+'\n')
print(f'{checks} package checks PASS; 12 exact candidate frame refs.')
