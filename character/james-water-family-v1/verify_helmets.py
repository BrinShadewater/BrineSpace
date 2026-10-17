from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;checks=0;fail=[]
def check(ok,msg):
 global checks
 checks+=1
 if not ok:fail.append(msg)
def pixels(f):return np.array(Image.open(f).convert('RGBA'))
for d in ['east','south','west','north']:
 p=P.parent/('james-water-'+d+'-v1');bare=json.loads((p/'bare-manifest.json').read_text());eq=json.loads((p/'helmet-manifest.json').read_text());reg=json.loads((p/'helmet-registration.json').read_text());hashes=json.loads((p/'helmet-hashes.json').read_text());frames={}
 check(hashlib.sha256((p/'source-helmet.png').read_bytes()).hexdigest()==reg['sourceSha256'],d+' source hash')
 check(len(set(t['fixedHeadScale'] for t in reg['tracking'].values()))==1,d+' fixed head scale')
 check(reg['masterShellWidth']=={'east':35,'south':39,'west':35,'north':33}[d],d+' calibrated shell ruler')
 for bs,s in zip(bare['states'],eq['states']):
  for key in ['id','loop','frameDurationsMs','waterPoses','waterKinds','facings','depthOffsets']:check(s[key]==bs[key],d+key+' paired')
  arrays=[]
  for j,(bf,ef) in enumerate(zip(bs['frameFiles'],s['frameFiles'])):
   b=pixels(p/bf);e=pixels(p/ef);arrays.append(e);i=str(s['provenance']['sourcePoses'][j]);record=reg['tracking'][i];x0,y0,x1,y1=record['editRegion'];outside=np.ones(e.shape[:2],bool);outside[y0:y1,x0:x1]=False
   check(np.array_equal(b[outside],e[outside]),ef+' exact body outside owned head');check(not np.array_equal(b,e),ef+' has helmet');check(not np.any(e[[0,-1],:,3]) and not np.any(e[:,[0,-1],3]),ef+' no clipping');check(hashlib.sha256((p/ef).read_bytes()).hexdigest()==hashes[ef],ef+' hash')
  frames[s['id']]=arrays
 for action in ['tread','swim']:check(np.array_equal(frames[action+'-'+d][0],frames[action+'-'+d][-1]),d+action+' seam')
 start=frames['swim-start-'+d];stop=frames['swim-stop-'+d]
 check(np.array_equal(start[0],frames['tread-'+d][0]),d+' equipped tread/start');check(np.array_equal(start[-1],frames['swim-'+d][0]),d+' equipped start/swim')
 for j in range(6):check(np.array_equal(start[j],stop[5-j]),d+' equipped reversed stop')
report=dict(checks=checks,failures=fail,status='PASS' if not fail else 'FAIL',scope='Staged shared-helmet composition and matching contracts; live water clearance/routes and installation unproven')
(P/'helmet-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(bool(fail))
