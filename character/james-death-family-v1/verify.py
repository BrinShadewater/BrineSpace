from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0;failures=[]
def check(ok,why):
 global checks
 checks+=1
 if not ok:failures.append(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pixels(p):return np.array(Image.open(p).convert('RGBA'))
retained=json.loads((P/'retained-contracts.json').read_text());hashes=json.loads((P/'frame-hashes.json').read_text());records=json.loads((P/'registration.json').read_text());states={}
for key,record in json.loads((P.parent/'james-air-family-v1/endpoint-sources.json').read_text()).items():check(sha(R/record['source'])==record['sourceSha256'],'Unchanged selected endpoint '+key)
for d,record in records.items():check(sha(P.parent/('james-death-'+d+'-v1')/'source.png')==record['sourceSha256'],'Selected source '+d)
for mode in ['bare','helmet']:
 m=json.loads((P/(mode+'-manifest.json')).read_text());states[mode]={s['id']:s for s in m['states']};check(len(states[mode])==8,'Eight states '+mode);check(m['pivot']==[128,224] and m['standingHeight']==148,'Physical pivot/density '+mode)
 for key,s in states[mode].items():
  old=retained[key]['state'];check(s['frameCount']==len(s['frameFiles'])==6,'Six poses '+key+mode)
  for field in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets','loop']:check(s[field]==old[field],'Retained '+field+key+mode)
  for i,rel in enumerate(s['frameFiles']):
   file=P/rel;a=pixels(file);check(a.shape==(360,256,4),'Canvas '+key+mode+str(i));y,x=np.where(a[:,:,3]>0);check(len(x)>0 and x.min()>0 and x.max()<255 and y.min()>0 and y.max()<359,'Nonclipped alpha '+key+mode+str(i));check(sha(file)==hashes[rel],'Pose hash '+key+mode+str(i))
  d=key.split('-')[-1];action=key.removesuffix('-'+d)
  check(np.array_equal(pixels(P/s['frameFiles'][0]),pixels(P.parent/'james-air-family-v1/endpoints'/mode/(('swim' if action=='death-water' else 'idle')+'-'+d+'.png'))),'Exact selected entry '+mode+key)
for d,record in records.items():
 for action,reg in record['actions'].items():
  check(sha(P.parent/('james-death-'+d+'-v1')/reg['sourceFile'])==reg['sourceSha256'],'Selected action source '+d+action)
  key=action+'-'+d
  for i,tracked in enumerate(reg['tracking']):
   if i==0:continue
   a=pixels(P/states['bare'][key]['frameFiles'][i]);b=pixels(P/states['helmet'][key]['frameFiles'][i]);x0,y0,x1,y1=tracked['editRegion'];outside=np.ones(a.shape[:2],bool);outside[max(0,y0):min(360,y1),max(0,x0):min(256,x1)]=False
   check(np.array_equal(a[outside],b[outside]),'Head-owned composition '+key+str(i));check(sha(P.parent/('james-water-'+d+'-v1')/'source-helmet.png')==tracked['helmetSourceSha256'],'Unchanged helmet donor '+key+str(i))
(P/'packaging-validation.json').write_text(json.dumps(dict(checks=checks,failures=failures,passed=not failures,scope='Package contracts, source/donor/endpoint provenance and ownership, not anatomy or installed behavior acceptance'),indent=2)+'\n');print(checks,'checks;',len(failures),'failures');print('\n'.join(failures[:12]));raise SystemExit(bool(failures))
