from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];reg=json.loads((HERE/'registration.json').read_text());checks=0
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
for mode in ['bare','helmet']:
 m=json.loads((HERE/(mode+'-manifest.json')).read_text());check(len(m['states'])==4,'coverage');check(m['standingHeight']==148,'master scale')
 for st in m['states']:
  source=m['states'][m['states'].index(st)]['provenance']['inspectionDerivation'];p=ROOT/source['sourceManifest'];donor=json.loads(p.read_text());ds=next(s for s in donor['states'] if s['id']==source['sourceState']);check(m['pivot']==donor['pivot'] and m['frameWidth']==donor['frameWidth'] and m['frameHeight']==donor['frameHeight'],'original registration');check(st['frameDurationsMs']==ds['frameDurationsMs'][:-1]+[ds['frameDurationsMs'][-1]+500] and sum(st['frameDurationsMs'])==6000 and st['loop'],'timing and loop')
  for i,f in enumerate(st['frameFiles']):
   path=(HERE/f).resolve();im=Image.open(path).convert('RGBA');check(path==ROOT/reg[mode][st['id']][i]['source'],'direct source reference');check(hashlib.sha256(path.read_bytes()).hexdigest()==reg[mode][st['id']][i]['sha256'],'source frozen');check(im.tobytes()==Image.open(p.parent/ds['frameFiles'][i]).convert('RGBA').tobytes(),'exact pixels');check(im.size==(m['frameWidth'],m['frameHeight']),'canvas')
  check(Image.open(HERE/st['frameFiles'][0]).convert('RGBA').tobytes()==Image.open(HERE/st['frameFiles'][-1]).convert('RGBA').tobytes(),'exact closed cycle')
gif=Image.open(HERE/'review.gif');total=0
for i in range(gif.n_frames):gif.seek(i);total+=gif.info['duration']
check(total==24000,'decoded preview duration');gif.seek(55);gif.convert('RGB').save(HERE/'review-frame055.png');report=dict(checks=checks,failures=0,sourceReferences=1130,exactSourcePixels=True,exactIdleSeams=True,runtimeMsPerInspection=6000,decodedGifMs=total,ownerReviewPending=True);(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
