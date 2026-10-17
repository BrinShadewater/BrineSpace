"""Measure visual envelopes against selected idle and prior recovery; no fake gate."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(path,pivot,standing):
 a=np.array(Image.open(path).convert('RGBA'));y,x=np.where(a[:,:,3]>20)
 return ((np.array([x.min(),y.min(),x.max()+1,y.max()+1])-np.tile(pivot,2))*(384*.17/standing)).tolist()
def union(rows):
 a=np.array(rows);return [float(a[:,0].min()),float(a[:,1].min()),float(a[:,2].max()),float(a[:,3].max())]
def covers(a,b):return all(a[i]<=b[i] if i<2 else a[i]>=b[i] for i in range(4))
audit=json.loads((ROOT/'character/veld-remaining-specials-audit-v1/inventory.json').read_text());records=[]
for gear in ['bare','helmet']:
 m=json.loads((P/f'{gear}-manifest.json').read_text())
 for s in m['states']:
  direction=s['id'].split('-')[-1];old=audit['selected'][gear][s['id']];idle=audit['selected'][gear]['idle-'+direction]
  # The source audit contains every actual ordered selected filename; reject changed inputs.
  for spec in [old,idle]:
   assert sha(ROOT/spec['manifest'])==spec['manifestHash'],'Selected authority changed;refresh audit before measuring'
   assert all(sha(ROOT/f)==h for f,h in zip(spec['files'],spec['frameHashes'])),'Selected pixels changed'
  frames=[]
  for file in s['frameFiles']:
   f=ROOT/file.removeprefix('res://');frames.append({'file':file,'sha256':sha(f),'bounds':bounds(f,m['pivot'],m['standingHeight'])})
  current=union([f['bounds'] for f in frames]);prior=union([bounds(ROOT/f,old['pivot'],old['standingHeight']) for f in old['files']]);standing=union([bounds(ROOT/f,idle['pivot'],idle['standingHeight']) for f in idle['files']])
  records.append({'gear':gear,'state':s['id'],'frames':frames,'candidateEnvelope':current,'priorRecoveryEnvelope':prior,'selectedIdleEnvelope':standing,'coveredByPriorRecovery':covers(prior,current),'coveredBySelectedIdle':covers(standing,current),'forwardReachChangeVsPrior':current[2]-prior[2] if direction=='east' else prior[0]-current[0] if direction=='west' else None})
report={'states':len(records),'references':sum(len(r['frames']) for r in records),'actualStandingScale':65.28,'alphaThreshold':20,'records':records,'recoveryGate':'CrewLife.pose selects dry idle recovery without calling clear();dry walking uses standing foot geometry. No recover-air entry is consumed from clearance.json. This is a visual-envelope audit, not route clearance proof.','runtimeProfileChanged':False}
(P/'clearance-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"{report['states']} states/{report['references']}refs measured;covered by prior recovery {sum(r['coveredByPriorRecovery'] for r in records)}/8;dry recovery has no profile gate")
for r in records:print(r['gear'],r['state'],'new',r['candidateEnvelope'],'prior',r['priorRecoveryEnvelope'])
