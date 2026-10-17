from pathlib import Path
import hashlib,json,itertools
from PIL import Image
HERE=Path(__file__).resolve().parent
packs={k:json.loads((HERE/f'{k}-manifest.json').read_text(encoding='utf-8')) for k in ['bare','helmet']}
provenance=json.loads((HERE/'half-turn-provenance.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/'frame-hashes.json').read_text(encoding='utf-8'));checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
keys={'swim-turn-'+a+'-'+b for a,b in itertools.permutations(['east','south','west','north'],2)}
for kind,pack in packs.items():
 check({s['id'] for s in pack['states']}==keys and len(pack['states'])==12,'full route matrix')
 check(pack['pivot']==[128,128] and pack['standingHeight']==148,'water registration')
 for s in pack['states']:
  half=kind+'/'+s['id'] in provenance;n=11 if half else 6
  check(len(s['frameFiles'])==n and all(len(s[field])==n for field in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets']),'per-frame metadata')
  check(not s['loop'] and sum(s['frameDurationsMs'])==(1280 if half else 640),'finite timing')
  for file in s['frameFiles']:
   im=Image.open(HERE/file);box=im.getchannel('A').getbbox();check(im.mode=='RGBA' and im.size==(256,256) and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'clearance')
  if half:
   p=provenance[kind+'/'+s['id']]
   for r in p['frames']:check((HERE/r['file']).read_bytes()==(HERE/r['source']).read_bytes() and hashlib.sha256((HERE/r['file']).read_bytes()).hexdigest()==hashes[r['file']],'derived source hashes')
   check((HERE/s['frameFiles'][5]).read_bytes()==(HERE/p['mergedSource']).read_bytes(),'exact common midpoint')
for a,b in zip(packs['bare']['states'],packs['helmet']['states']):check(a['id']==b['id'] and a['frameDurationsMs']==b['frameDurationsMs'],'gear clocks')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'12route matrix pergear,exact source/midpoint pixels,registration/clearance/clocks;native and visual separate'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} water carry matrix checks PASS')
