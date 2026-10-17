"""Staged water packaging contracts; not a visual or live-route acceptance test."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from build import protection
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0;fail=[]
def check(ok,msg):
 global checks
 checks+=1
 if not ok:fail.append(msg)
def pixels(f):return np.array(Image.open(f).convert('RGBA'))
family=json.loads((P/'bare-manifest.json').read_text());check(len(family['states'])==16,'16 water states')
for d in ['east','south','west','north']:
 p=P.parent/('james-water-'+d+'-v1');m=json.loads((p/'bare-manifest.json').read_text());reg=json.loads((p/'registration.json').read_text());hashes=json.loads((p/'frame-hashes.json').read_text());st={s['id']:s for s in m['states']};frames={sid:[pixels(p/f) for f in s['frameFiles']] for sid,s in st.items()}
 check(m['pivot']==[128,128] and m['standingHeight']==148,d+' world registration')
 for name,h in reg['sourceHashes'].items():check(hashlib.sha256((p/name).read_bytes()).hexdigest()==h,d+' source '+name)
 for source in reg['sourceHashes']:check(len(set(t['fixedScale'] for t in reg['tracking'] if t['source']==source))==1,d+' fixed source scale '+source)
 for sid,s in st.items():
  check(len(s['frameFiles'])==6 and len(s['frameDurationsMs'])==6,sid+' six slots')
  check(s['facings']==[d]*6,sid+' facing');check(s['waterPoses']==[True]*6,sid+' water pose')
  expectedloop=sid.split('-'+d)[0] in ['tread','swim'];check(s['loop']==expectedloop,sid+' loop contract')
  for j,f in enumerate(s['frameFiles']):
   a=frames[sid][j];check(a.shape==(276,256,4),f+' dimensions');check(np.any(a[:,:,3]>180),f+' visible body');check(not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3]),f+' no clipping');check(hashlib.sha256((p/f).read_bytes()).hexdigest()==hashes[f],f+' hash')
   i=s['provenance']['sourcePoses'][j];raw=pixels(p/'registered-ungraded'/f'{i:03d}.png');mask=protection((256,276),reg['tracking'][i]['headAnchor'],d)
   check(np.array_equal(a[:,:,3],raw[:,:,3]),f+' exact alpha through grade');check(np.array_equal(a[:,:,:3][mask],raw[:,:,:3][mask]),f+' protected original head')
 for action in ['tread','swim']:check(np.array_equal(frames[action+'-'+d][0],frames[action+'-'+d][-1]),d+action+' loop seam')
 start=frames['swim-start-'+d];stop=frames['swim-stop-'+d]
 check(np.array_equal(start[0],frames['tread-'+d][0]),d+' exact tread/start endpoint');check(np.array_equal(start[-1],frames['swim-'+d][0]),d+' exact start/swim endpoint')
 for j in range(6):check(np.array_equal(start[j],stop[5-j]),d+' exact reversed stop '+str(j))
report=dict(checks=checks,failures=fail,status='PASS' if not fail else 'FAIL',scope='Bare staged extraction/material/registration packaging; visual continuity, helmets, native water clearance/routes and runtime installation remain separate')
(P/'packaging-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(bool(fail))
