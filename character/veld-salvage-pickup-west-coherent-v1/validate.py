from pathlib import Path
import json,hashlib
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];checks=0;hashes={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok):
 global checks
 checks+=1;assert ok,checks
fit=json.loads((H/'fit-checks.json').read_text());native=json.loads((H/'native-candidate-v1-checks.json').read_text())
for g in ['bare','helmet']:
 m=json.loads((H/f'{g}-manifest.json').read_text());old=json.loads((R/f'character/dr-veld-v2/packs/{g}-256x256-p128.0-128.0/manifest.json').read_text());byid={s['id']:s for s in m['states']}
 check(m['pivot']==[128,128] and m['frameWidth']==m['frameHeight']==256 and m['standingHeight']==148 and m['precomposed'])
 for s in m['states']:
  original=next(x for x in old['states'] if x['id']==s['id']);check({k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in original.items() if k!='frameFiles'})
  for f in s['frameFiles']:
   im=Image.open(H/f);check(im.mode=='RGBA' and im.size==(256,256));hashes[f]=sha(H/f);check(hashes[f]==fit['frameHashes'][f])
 check(Image.open(H/byid['salvage-west']['frameFiles'][0]).tobytes()==Image.open(H/byid['swim-pickup-west']['frameFiles'][0]).tobytes())
 check(Image.open(H/byid['swim-pickup-west']['frameFiles'][5]).tobytes()==Image.open(R/fit['endpoints'][g]['cargo']).tobytes())
check(hashes==native['frameHashes']);check(native['failures']==0 and native['engine_errors']==[] and native['real_profile_changed_files']==[])
check(all(sha(H/f)==h for f,h in fit['sourceHashes'].items()));check(sha(R/'character/veld-swim-carry-west-coherent-v1/fit-checks.json')==fit['frozenCargoFitSha256'])
(H/'packaging-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,frameHashes=hashes,scope='Original state contracts, frozen recipe and source hashes, exact24refs/current native evidence and work/pickup/cargo endpoints; controller/world acceptance separate'),indent=2)+'\n')
print(f'{checks} package checks PASS;24exact paired action refs.')
