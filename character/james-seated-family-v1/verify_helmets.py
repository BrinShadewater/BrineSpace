from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;checks=0
def check(ok,why):
 global checks
 assert ok,why
 checks+=1
bare=json.loads((HERE/'bare-manifest.json').read_text());eq=json.loads((HERE/'helmet-manifest.json').read_text());tracking=json.loads((HERE/'helmet-registration.json').read_text());hashes=json.loads((HERE/'helmet-hashes.json').read_text())
for bs,es in zip(bare['states'],eq['states']):
 for k in ['id','frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']:check(bs[k]==es[k],'paired '+k)
 for i,(b,e) in enumerate(zip(bs['frameFiles'],es['frameFiles'])):
  ba=np.array(Image.open(HERE/b).convert('RGBA'));ea=np.array(Image.open(HERE/e).convert('RGBA'));rec=tracking[es['id']][i];cut=rec['headCutoff'];check(ea.shape==(192,184,4),'canvas');check(hashlib.sha256((HERE/e).read_bytes()).hexdigest()==hashes[e],'hash');check(rec['nativeScale']==1,'native shell scale')
  if rec['exactStandingMaster']:
   donor=Image.open(rec['donor']).convert('RGBA');check(np.array_equal(ea[:184],np.array(donor)),'exact selected standing master')
  else:check(np.array_equal(ba[cut:],ea[cut:]),'body below head unchanged')
  check(not ea[0,:,3].any() and not ea[-1,:,3].any() and not ea[:,0,3].any() and not ea[:,-1,3].any(),'head/body unclipped')
for d in ['east','south','west','north']:
 states={s['id']:s for s in eq['states']};down=states['sit-down-'+d];up=states['sit-rise-'+d]
 for a,b in zip(down['frameFiles'],reversed(up['frameFiles'])):check(Image.open(HERE/a).tobytes()==Image.open(HERE/b).tobytes(),'exact equipped rise reversal')
 for act in ['sit-idle','read-seated']:
  st=states[act+'-'+d];check(Image.open(HERE/st['frameFiles'][0]).tobytes()==Image.open(HERE/st['frameFiles'][-1]).tobytes(),'equipped loop');check(Image.open(HERE/st['frameFiles'][0]).tobytes()==Image.open(HERE/down['frameFiles'][-1]).tobytes(),'shared seat')
report=dict(checks=checks,failures=0,references=96,nativeHeadScale=1,protectedBody=True,ownerReviewPending=True)
(HERE/'helmet-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(checks,'helmet checks,0 failures')
