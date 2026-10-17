from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;checks=0;failures=[]
def check(ok,why):
 global checks
 checks+=1
 if not ok:failures.append(why)
def pixels(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
retained=json.loads((P/'retained-contracts.json').read_text());hashes=json.loads((P/'frame-hashes.json').read_text());manifests={}
for mode in ['bare','helmet']:
 m=json.loads((P/(mode+'-manifest.json')).read_text());states={s['id']:s for s in m['states']};manifests[mode]=states
 check(m['pivot']==[128,128] and m['standingHeight']==148,'Common pivot and height '+mode)
 check(m['strideDistanceCells']=={'swim-carry':retained['swim-carry-east']['pack']['strideDistanceCells']['swim-carry']},'Only retained cargo stride override '+mode)
 for key,s in states.items():
  old=retained[key]['state'];check(s['frameCount']==6==len(s['frameFiles']),'Frame count '+key+mode)
  for field in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets','loop']:check(s[field]==old[field],'Retained '+field+key+mode)
  for i,rel in enumerate(s['frameFiles']):
   f=P/rel;a=pixels(f);check(a.shape==(276,256,4),'Canvas '+key+mode+str(i));y,x=np.where(a[:,:,3]>0)
   check(len(x)>0 and x.min()>0 and x.max()<255 and y.min()>0 and y.max()<275,'Nonclipped alpha '+key+mode+str(i));check(sha(f)==hashes[rel],'Hash '+key+mode+str(i))
  if s['loop']:check(np.array_equal(pixels(P/s['frameFiles'][0]),pixels(P/s['frameFiles'][-1])),'Exact neutral loop '+key+mode)
 for d in ['east','south','west','north']:
  if 'salvage-'+d not in states:continue
  for a,b in [('salvage','swim-pickup'),('swim-pickup','swim-carry')]:
   check(np.array_equal(pixels(P/states[a+'-'+d]['frameFiles'][0 if a=='salvage' else -1]),pixels(P/states[b+'-'+d]['frameFiles'][0])),'Exact action join '+d+a+b+mode)
for d in ['east','south','west','north']:
 if 'salvage-'+d not in manifests['bare']:continue
 p=P.parent/('james-water-cargo-'+d+'-v1');reg=json.loads((p/'registration.json').read_text());check(sha(p/'source.png')==reg['sourceSha256'],'Selected source hash '+d)
 for action in ['salvage','swim-pickup','swim-carry']:
  bare=manifests['bare'][action+'-'+d];helm=manifests['helmet'][action+'-'+d]
  for j,i in enumerate(bare['provenance']['sourcePoses']):
   a=pixels(P/bare['frameFiles'][j]);b=pixels(P/helm['frameFiles'][j]);x0,y0,x1,y1=reg['helmetTracking'][i]['editRegion'];outside=np.ones(a.shape[:2],bool);outside[max(0,y0):min(276,y1),max(0,x0):min(256,x1)]=False;check(np.array_equal(a[outside],b[outside]),'Owned head only '+d+action+str(j))
report=dict(checks=checks,failures=failures,passed=not failures,statesPerMode=len(manifests['bare']),scope='Staged pixel contracts, retained clocks, neutral loops, exact salvage/pickup/carry joins and owned-head edits. No live route or owner acceptance claim.')
(P/'packaging-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(checks,'packaging checks;',len(failures),'failures;',len(manifests['bare']),'states/mode')
for f in failures[:12]:print(f)
raise SystemExit(bool(failures))
