from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;checks=[]
def check(ok,label):checks.append({'passed':bool(ok),'check':label})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((P/'manifest.json').read_text());r=json.loads((P/'registration.json').read_text());s=m['states'][0];h=json.loads((P/'frame-hashes.json').read_text())
check(sha(P/'sources/lateral-v1.png')==r['sourceSha256'],'Raw source binding')
idle=P.parent/'bill-seated-south-coherent-v1/frames/sit-down-south/000.png'
check(sha(idle)==r['idleSha256'] and Image.open(idle).tobytes()==Image.open(P/s['frameFiles'][0]).tobytes(),'Exact selected idle entry')
check(m['pivot']==[128,224] and m['standingHeight']==148 and m['status']=='staged_candidate' and m['precomposed'],'Shared standing contract')
check(not s['loop'] and sum(s['frameDurationsMs'])==2000 and s['terminalFrame']==5 and len(s['frameFiles'])==6,'Finite two-second six-slot terminal collapse')
check(s['facings']==['south']*6 and s['waterKinds']==['death-ground']*6 and s['waterPoses']==[False]*6 and s['depthOffsets']==[0]*6,'Directional dry metadata')
crowns=[]
for i,f in enumerate(s['frameFiles']):
 a=np.array(Image.open(P/f));y,x=np.where(a[:,:,3]>180);crowns.append(int(y.min()))
 check(a.shape==(256,256,4) and x.min()>0 and x.max()<255 and y.min()>0 and y.max()<255,'Whole figure contained '+str(i))
 check(sha(P/f)==h[f],'Bound pixels '+str(i))
check(r['fixedRuler']==[.29,.342] and [row['target'] for row in r['frames']]==[[128,223],[128,223],[84,223],[84,223],[84,223]],'Fixed anatomical ruler and authored lateral floor contacts')
check(abs(crowns[5]-crowns[4])<=3,'Small authored terminal settlement')
check(all(row['position'][0]>=0 and row['position'][0]+row['size'][0]<=256 and row['position'][1]>=0 and row['position'][1]+row['size'][1]<=256 for row in r['frames']),'Unclipped extraction bounds')
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'crowns':crowns,'scope':'authored source and finite terminal candidate; full master polish/paired equipment/actual dry mortality integration pending'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'checks':len(checks),'crowns':crowns}));raise SystemExit(0 if result['passed'] else 1)
