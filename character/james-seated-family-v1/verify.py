"""Validate staged source registration and seated transition contracts."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
pack=json.loads((HERE/'bare-manifest.json').read_text());checks=0;metrics={}
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
states={s['id']:s for s in pack['states']}
catalog=HERE.parents[1]/'character/chief-engineer-branforth-v2';retained={}
for f in json.loads((catalog/'catalog.json').read_text())['body']:
 for s in json.loads((catalog/f).read_text())['states']:retained[s['id']]=s
for s in pack['states']:
 for field in ['depthOffsets','waterKinds','waterPoses']:check(s[field]==retained[s['id']][field],'retained furniture '+field)
 ims=[Image.open(HERE/f).convert('RGBA') for f in s['frameFiles']]
 check(len(ims)==6,'six frames')
 check(sum(s['frameDurationsMs'])==(800 if s['id'].startswith(('sit-down','sit-rise')) else 1500 if s['id'].startswith('sit-idle') else 2600),'timing')
 measure=[]
 for im in ims:
  a=np.array(im);y,x=np.where(a[:,:,3]>180)
  check(im.size==(184,192),'canvas')
  check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any(),'clearance')
  check(170<=y.max()<=172,'registered sole')
  measure.append(int(y.max()-y.min()+1))
 metrics[s['id']]=measure
 if s['loop']:check(ims[0].tobytes()==ims[-1].tobytes(),'loop closes')
for d in ['east','south','west','north']:
 down=states['sit-down-'+d];up=states['sit-rise-'+d]
 for a,b in zip(down['frameFiles'],reversed(up['frameFiles'])):
  check(Image.open(HERE/a).tobytes()==Image.open(HERE/b).tobytes(),'exact reverse')
 for act in ['sit-idle','read-seated']:
  check(Image.open(HERE/down['frameFiles'][-1]).tobytes()==Image.open(HERE/states[act+'-'+d]['frameFiles'][0]).tobytes(),'shared seat')
report=dict(checks=checks,failures=0,status='staged_bare_only',metrics=metrics,helmetFitPending=True,runtimeBindingsUnchanged=True)
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(checks,'checks,0 failures,16 staged bare states')
