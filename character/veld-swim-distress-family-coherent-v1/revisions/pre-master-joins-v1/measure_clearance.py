"""Audit the actual effective base-swim/life-distress footprint for all poses."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];file=R/'character/dr-veld-v2/clearance.json';c=json.loads(file.read_text());rows=[]
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text())
 for s in m['states']:
  d=s['id'].split('-')[-1];base=c['swim'][gear][d];additional=c['life'][gear][s['id']]
  effective=[min(base[i],additional[i]) if i<2 else max(base[i],additional[i]) for i in range(4)];bounds=[]
  for f in s['frameFiles']:
   a=np.array(Image.open(P/f));y,x=np.where(a[:,:,3]>20)
   bounds.append(((np.array([x.min(),y.min(),x.max()+1,y.max()+1])-np.array(m['pivot']*2))*65.28/m['standingHeight']).tolist())
  b=np.array(bounds);candidate=[float(b[:,0].min()),float(b[:,1].min()),float(b[:,2].max()),float(b[:,3].max())]
  covered=all(effective[i]<=candidate[i] if i<2 else effective[i]>=candidate[i] for i in range(4))
  proposed=[min(additional[i],candidate[i]) if i<2 else max(additional[i],candidate[i]) for i in range(4)]
  rows.append({'gear':gear,'state':s['id'],'frames':bounds,'candidateEnvelope':candidate,'currentBaseSwim':base,'currentLifeAdditional':additional,'currentEffectiveConsumedExtent':effective,'coveredByCurrentConsumedExtent':covered,'additionalWouldBeNeededIfNotCovered':proposed if not covered else None})
report={'states':8,'references':48,'alphaThreshold':20,'stationStandingHeight':65.28,'selectedProfileSha256':hashlib.sha256(file.read_bytes()).hexdigest(),'rows':rows,'profileChanged':False,'scope':'actual consumed union contains alpha envelope; not furniture occlusion/controller/owner acceptance'}
(P/'clearance-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'Current consumed profile covers {sum(r["coveredByCurrentConsumedExtent"] for r in rows)}/8 gear states; no profile edits')
for r in rows:
 if not r['coveredByCurrentConsumedExtent']:print(r['gear'],r['state'],'candidate',r['candidateEnvelope'],'current',r['currentEffectiveConsumedExtent'])
