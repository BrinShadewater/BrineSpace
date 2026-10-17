from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0;failures=[]
def check(ok,label):
 global checks
 checks+=1
 if not ok:failures.append(label)
def pixels(ref):return np.array(Image.open(R/ref[6:]).convert('RGBA'))
bindings=json.loads((P/'source-bindings.json').read_text())
for mode in ['bare','helmet']:
 pack=json.loads((P/(mode+'-manifest.json')).read_text());states={s['id']:s for s in pack['states']}
 check(len(states)==12,mode+' three phases/four directions')
 for b in [x for x in bindings if x['mode']==mode]:
  d=b['direction'];enter=states['read-seated-enter-'+d];held=states['read-seated-'+d];exit=states['read-seated-exit-'+d]
  for source in b['sources']:check(hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256'],mode+d+' frozen authored source')
  check(sum(enter['frameDurationsMs'])==480 and sum(exit['frameDurationsMs'])==480,mode+d+' draw/stow clock')
  check(sum(held['frameDurationsMs'])==3600 and held['loop'] and not enter['loop'] and not exit['loop'],mode+d+' held clock and one-shot phases')
  check(enter['frameFiles']==exit['frameFiles'][::-1],mode+d+' exact draw/stow reversal')
  check(enter['frameFiles'][-1]==held['frameFiles'][0]==exit['frameFiles'][0],mode+d+' exact supported reading joins')
  check(enter['frameFiles'][0]==exit['frameFiles'][-1]=='res://'+b['sources'][0]['path'],mode+d+' exact seated neutral joins')
  for s in [enter,held,exit]:
   for field in b['state']:
    if field not in ['id','frameFiles','frameDurationsMs','loop','depthOffsets','provenance']:check(s.get(field)==b['state'][field],mode+s['id']+' retained '+field)
   check(all(ref.startswith('res://') for ref in s['frameFiles']),mode+s['id']+' complete resource paths')
   check(all(np.any(pixels(ref)[:,:,3]>192) for ref in s['frameFiles']),mode+s['id']+' nonempty sources')
(P/'packaging-validation.json').write_text(json.dumps({'checks':checks,'failures':failures,'references':144,'scope':'Whole-source alias hashes, exact entry/held/reverse-exit/neutral joins, retained metadata and .48/11.04/.48 controller contract; no newly authored drawing count or native acceptance.'},indent=2)+'\n');print(json.dumps({'checks':checks,'failures':failures}));raise SystemExit(bool(failures))
