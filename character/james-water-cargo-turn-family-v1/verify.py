from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0;failures=[]
def check(ok,why):
 global checks
 checks+=1
 if not ok:failures.append(why)
def pixels(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
retained=json.loads((P/'retained-contracts.json').read_bytes());hashes=json.loads((P/'frame-hashes.json').read_bytes());records=json.loads((P/'registration.json').read_bytes());manifests={}
for pair,reg in records.items():
 p=P.parent/('james-water-cargo-turn-'+pair+'-v1')
 check(sha(p/'source.png')==reg['sourceSha256'],'Selected source hash '+pair)
 for tracked in reg['tracking']:
  helmet=tracked['helmet']
  if not helmet.get('exactEndpoint'):
   check(sha(p/helmet['sourceFile'])==helmet['sourceSha256'],'Selected helmet donor hash '+pair+str(helmet['sourceHead']))
 for mode in ['bare','helmet']:
  check((p/(mode+'-endpoint-reference.png')).exists(),'Preserved actual endpoint reference '+pair+mode)
  for d in json.loads((p/(mode+'-endpoints.json')).read_bytes()):check(sha(R/d['file'])==d['sha256'],'Exact unchanged endpoint source '+d['direction']+mode)
for mode in ['bare','helmet']:
 m=json.loads((P/(mode+'-manifest.json')).read_bytes());states={s['id']:s for s in m['states']};manifests[mode]=states
 check(len(states)==12,'Twelve turn states '+mode);check(sum(len(s['frameFiles']) for s in states.values())==92,'92 selected refs '+mode)
 check(m['pivot']==[128,128] and m['standingHeight']==148,'Common world pivot and physical scale '+mode)
 for key,s in states.items():
  half=s['frameCount']==11;check(s['frameCount']==len(s['frameFiles']),'Frame count '+key+mode)
  check(sum(s['frameDurationsMs'])==(1600 if half else 800),'Consistent quarter/half angular pace '+key+mode)
  check(s['loop']==False,'One shot '+key+mode)
  for field in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets']:check(len(s[field])==s['frameCount'],'Metadata count '+field+key+mode)
  for i,rel in enumerate(s['frameFiles']):
   f=P/rel;a=pixels(f);check(a.shape==(276,256,4),'Canvas '+key+mode+str(i));y,x=np.where(a[:,:,3]>0)
   check(len(x)>0 and x.min()>0 and x.max()<255 and y.min()>0 and y.max()<275,'Nonclipped alpha '+key+mode+str(i))
   check(sha(f)==hashes[rel],'Selected pose hash '+key+mode+str(i))
  old=retained[key]['state']
  for field in ['frameDurationsMs','facings','waterKinds','waterPoses','depthOffsets']:
   expected=list(old[field])
   if half:
    if field=='frameDurationsMs':
     parts=s['provenance']['timingQuarterSources']
     first=states['swim-carry-turn-'+parts[0]][field]
     second=states['swim-carry-turn-'+parts[1]][field]
     expected=first[:-1]+[first[-1]+second[0]]+second[1:]
    else:del expected[6]
   check(s[field]==expected,'Retained contract with exact merged seam '+field+key+mode)
  directions=key.split('-')[3:]
  for i,d in [(0,directions[0]),(-1,directions[1])]:
   folder=P.parent/('james-water-cargo-'+d+'-v1');em=json.loads((folder/(mode+'-manifest.json')).read_bytes());es=next(q for q in em['states'] if q['id']=='swim-carry-'+d)
   check(np.array_equal(pixels(P/s['frameFiles'][i]),pixels(folder/es['frameFiles'][0])),'Exact installed swim endpoint '+key+mode+str(i))
  reverse=states['swim-carry-turn-'+directions[1]+'-'+directions[0]]
  for a,b in zip(s['frameFiles'],reversed(reverse['frameFiles'])):check(np.array_equal(pixels(P/a),pixels(P/b)),'Exact reversed selected pose '+key+mode)
for pair,reg in records.items():
 bare=manifests['bare']['swim-carry-turn-'+pair];helm=manifests['helmet']['swim-carry-turn-'+pair]
 for i in range(1,5):
  a=pixels(P/bare['frameFiles'][i]);b=pixels(P/helm['frameFiles'][i]);x0,y0,x1,y1=reg['tracking'][i]['helmet']['editRegion'];outside=np.ones(a.shape[:2],bool);outside[max(0,y0):min(276,y1),max(0,x0):min(256,x1)]=False
  check(np.array_equal(a[outside],b[outside]),'Owned-head edit only '+pair+str(i))
report=dict(checks=checks,failures=failures,passed=not failures,scope='Staged package contracts, preserved endpoints, exact reverse/composition and head ownership. Does not certify live-route clearance or owner acceptance.')
(P/'packaging-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(str(checks)+' packaging checks; '+str(len(failures))+' failures')
for f in failures[:15]:print(f)
raise SystemExit(bool(failures))
