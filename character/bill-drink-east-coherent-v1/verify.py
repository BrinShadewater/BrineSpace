from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(ok,label):checks.append({'passed':bool(ok),'check':label})
r=json.loads((P/'registration.json').read_text());cfg=json.loads((P/'source-rulers.json').read_text());m=json.loads((P/'manifest.json').read_text());s=m['states'][0]
check(sha(P/r['source'])==r['sourceSha256'],'Raw source binding')
check(r['fixedRuler']==cfg['fixedRuler'] and r['heads']==cfg['heads'],'Frozen whole-atlas ruler/head axes')
check(sha(P.parent/r['idleAuthority'])==r['idleSha256'],'Selected matte master binding')
check(max(row['headAxis'][1] for row in r['frames'])-min(row['headAxis'][1] for row in r['frames'])<=2,'Upright crown range within two native pixels')
check(len({tuple(row['targetFrontBoot']) for row in r['frames']})==1,'Fixed master planted sole/front boot')
check(m['pivot']==[128,224] and m['standingHeight']==148 and m['status']=='staged_candidate','Shared standing density/candidate scope')
check(s['loop'] and sum(s['frameDurationsMs'])==960 and len(s['frameFiles'])==7,'Seven-slot authored960ms cycle')
check(s['id']=='drink-east' and s['waterKinds']==['drink']*7 and s['facings']==['east']*7,'Directional drinking identity')
images=[np.array(Image.open(P/f).convert('RGBA')) for f in s['frameFiles']]
check(np.array_equal(images[0],images[-1]),'Exact whole-pose closure')
check(len({a.tobytes() for a in images})==6,'Six distinct authored meal poses')
for f,a in zip(s['frameFiles'],images):
    check(sha(P/f)==json.loads((P/'frame-hashes.json').read_text())[f],'Frame binding '+f)
    y,x=np.where(a[:,:,3]>180)
    check(a.shape==(256,256,4) and y.max()==223 and x.min()>0 and x.max()<255,'Contained planted sole '+f)
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'scope':'source/grade/ruler/loop candidate; cup pickup/return and normal service installation pending'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));raise SystemExit(0 if result['passed'] else 1)
