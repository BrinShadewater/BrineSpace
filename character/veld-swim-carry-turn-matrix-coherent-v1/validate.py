from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];checks=0;hashes={};bounds={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v):
 global checks
 assert v;checks+=1
def pixels(p):
 with Image.open(p) as im:return im.tobytes()
pr=json.loads((H/'provenance.json').read_text());pairs={}
for familygear,files in pr['sourceBindings'].items():
 family,_=familygear.split('/');folder=R/f'character/veld-swim-carry-turn-{family}-coherent-v1'
 for f,h in files.items():check(sha(folder/f)==h)
for gear in ['bare','helmet']:
 m=json.loads((H/f'{gear}-manifest.json').read_text());old=json.loads((R/f'character/dr-veld-v2/packs/{gear}-256x256-p128.0-128.0/manifest.json').read_text());original={s['id']:s for s in old['states']};check(m['pivot']==[128,128] and m['standingHeight']==148 and m['precomposed']);check(len(m['states'])==12);states={s['id']:s for s in m['states']};pairs[gear]=states
 for key,s in states.items():
  p=pr['states'][gear+'/'+key];half=bool(p['route']);check({k:v for k,v in s.items() if k!='frameFiles'}=={k:v for k,v in original[key].items() if k!='frameFiles'});check(not s['loop']);check(len(s['frameFiles'])==(12 if half else 6));check(sum(s['frameDurationsMs'])==(680 if half else 800))
  for f,r in zip(s['frameFiles'],p['frames']):
   with Image.open(H/f) as im:check(im.size==(256,256) and im.mode=='RGBA');a=np.array(im)
   check(pixels(H/f)==pixels(R/r['source']));check(sha(H/f)==r['sha256']);check(not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20));hashes[f]=sha(H/f);y,x=np.where(a[:,:,3]>20);bounds[f]=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  start,end=key.removeprefix('swim-carry-turn-').split('-')
  for d,f in [(start,s['frameFiles'][0]),(end,s['frameFiles'][-1])]:check(pixels(H/f)==pixels(R/f'character/veld-swim-carry-{d}-coherent-v1/frames/{gear}/swim-carry-{d}/000.png'))
  reverse=states[f'swim-carry-turn-{end}-{start}'];check(s['frameDurationsMs']==list(reversed(reverse['frameDurationsMs'])));check(all(pixels(H/a)==pixels(H/b) for a,b in zip(s['frameFiles'],reversed(reverse['frameFiles']))))
  if half:check(pixels(H/s['frameFiles'][5])==pixels(H/s['frameFiles'][6]));check(s['frameDurationsMs'][5]+s['frameDurationsMs'][6]==90)
for key,b in pairs['bare'].items():
 for f in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets','loop']:check(b[f]==pairs['helmet'][key][f])
(H/'validation-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,frameHashes=hashes,manifestHashes={g:sha(H/f'{g}-manifest.json') for g in pairs},provenanceSha256=sha(H/'provenance.json'),scope='192 exact source-derived refs/original contracts/cardinal joins/reverses/paired clocks; full motion and world acceptance separate'),indent=2)+'\n',encoding='utf-8');(H/'alpha-bounds-v1.json').write_text(json.dumps(dict(alphaThreshold=20,pivot=[128,128],standingHeight=148,frameBounds=bounds,scope='Measured frames only; world clearance not proved'),indent=2)+'\n',encoding='utf-8');print(f'{checks} full cargo matrix package/source checks PASS')
