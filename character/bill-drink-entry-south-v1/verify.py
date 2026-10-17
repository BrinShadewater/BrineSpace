from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;checks=[]
def check(ok,why):checks.append({'passed':bool(ok),'check':why})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((P/'registration.json').read_text());cfg=json.loads((P/'source-rulers.json').read_text());m=json.loads((P/'manifest.json').read_text());enter,exit=m['states']
for key,spec in r['sources'].items():check(sha(P/spec['source'])==r['sourcesSha256'][key],'Raw source binding '+key)
check(r['sources']==cfg['sources'] and r['sequence']==cfg['sequence'],'Frozen source rulers and explicit five-pose selection')
check(max(row['headAxis'][1] for row in r['frames'])-min(row['headAxis'][1] for row in r['frames'])<=2,'Interior standing crown range <=2px')
check(len(r['frames'])==5 and len({(row['source'],row['sourcePose']) for row in r['frames']})==5,'Five authored interiors include missing short reach')
check(len({tuple(row['targetFrontBoot']) for row in r['frames']})==1,'Fixed master sole/front-boot registration')
for file,digest in json.loads((P/'frame-hashes.json').read_text()).items():check(sha(P/file)==digest,'Frame binding '+file)
check(m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'] and m['status']=='staged_candidate','Shared candidate figure plane')
check(exit['frameFiles']==enter['frameFiles'][::-1] and exit['frameDurationsMs']==enter['frameDurationsMs'][::-1],'Exact reverse return')
check(sum(enter['frameDurationsMs'])==580 and not enter['loop'] and not exit['loop'],'Finite580ms pickup/return')
for state,kind in zip(m['states'],['drink-enter','drink-exit']):check(state['waterKinds']==[kind]*7 and state['facings']==['south']*7 and state['depthOffsets']==[0]*7 and state['waterPoses']==[False]*7,'Directional dry metadata '+kind)
for donor,index in zip(r['donors'],[0,-1]):
    path=P.parent/donor['path'];check(sha(path)==donor['sha256'],'Endpoint source binding')
    check(Image.open(P/enter['frameFiles'][index]).convert('RGBA').tobytes()==Image.open(path).convert('RGBA').tobytes(),'Exact selected idle/held endpoint')
for file in enter['frameFiles']:
    a=np.array(Image.open(P/file));y,x=np.where(a[:,:,3]>180);check(a.shape==(256,256,4) and y.max()==223 and x.min()>0 and x.max()<255,'Planted sole/contained whole figure '+file)
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'scope':'candidate source/fixed rulers/finite joins; normal drink service/counter/restore pending'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));raise SystemExit(0 if result['passed'] else 1)
