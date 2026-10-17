"""Audit every candidate frame against live selected movement/action bounds."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];path=R/'character/dr-veld-v2/clearance.json';selected=json.loads(path.read_text());records=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def union(a,b):return [min(a[i],b[i]) if i<2 else max(a[i],b[i]) for i in range(4)]
def covered(a,b):return all(a[i]<=b[i] if i<2 else a[i]>=b[i] for i in range(4))
for family in ['veld-swim-carry-matrix-coherent-v1','veld-salvage-pickup-family-coherent-v1','veld-swim-carry-turn-matrix-coherent-v1']:
 for gear in ['bare','helmet']:
  p=R/f'character/{family}/{gear}-manifest.json';m=json.loads(p.read_text());scale=384*.17/m['standingHeight'];pivot=np.tile(m['pivot'],2)
  for s in m['states']:
   d=s['id'].split('-')[-1];movement=selected['swim'][gear][d];kind='transition' if s['id'].startswith('swim-carry-turn-') else ('swim-carry' if s['id'].startswith('swim-carry-') else 'salvage');action=selected['life'][gear]['cargo-turn-'+d] if kind=='transition' else selected['actions'][gear][kind+'-'+d];effective=union(movement,action);frames=[]
   for f in s['frameFiles']:
    fp=R/f.removeprefix('res://') if f.startswith('res://') else p.parent/f
    a=np.array(Image.open(fp).convert('RGBA'));y,x=np.where(a[:,:,3]>20);b=((np.array([x.min(),y.min(),x.max()+1,y.max()+1])-pivot)*scale).tolist();frames.append(dict(file=fp.relative_to(R).as_posix(),sha256=sha(fp),nativeBounds=b,coveredByMovement=covered(movement,b),coveredByEffectiveAction=covered(effective,b)))
   b=np.array([f['nativeBounds'] for f in frames]);extent=[float(b[:,0].min()),float(b[:,1].min()),float(b[:,2].max()),float(b[:,3].max())];records.append(dict(family=family,gear=gear,state=s['id'],scale=scale,movementBounds=movement,actionKey=('cargo-turn-' if kind=='transition' else kind+'-')+d,actionSection='life' if kind=='transition' else 'actions',effectiveActionBounds=effective,nativeUnion=extent,coveredByMovement=covered(movement,extent),coveredByEffectiveAction=covered(effective,extent),frames=frames,manifestSha256=sha(p)))
report=dict(installed=False,selectedClearanceSha256=sha(path),states=len(records),references=sum(len(r['frames']) for r in records),movementUndercovered=sum(not r['coveredByMovement'] for r in records),effectiveActionUndercovered=sum(not r['coveredByEffectiveAction'] for r in records),scope='All candidate alpha envelopes at actual65.28unit standing scale. Movement vs effective action compared separately; no world-route acceptance or safety mutation.',records=records)
(H/'candidate-clearance-v1.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(f"{report['states']} states/{report['references']} refs measured; movement undercovered{report['movementUndercovered']}, effective action undercovered{report['effectiveActionUndercovered']}")
for r in records:
 if not r['coveredByMovement'] or not r['coveredByEffectiveAction']:print(r['gear'],r['state'],'movement',r['coveredByMovement'],'action',r['coveredByEffectiveAction'])

proposal=copy.deepcopy(selected)
for r in records:
 gear=r['gear'];d=r['state'].split('-')[-1];extent=r['nativeUnion'];section=r['actionSection'];key=r['actionKey'];proposal[section][gear][key]=union(proposal[section][gear][key],extent)
 if r['state'].startswith('swim-carry-') and not r['state'].startswith('swim-carry-turn-'):proposal['swim'][gear][d]=union(proposal['swim'][gear][d],extent)
(H/'candidate-clearance-profile-v1.json').write_text(json.dumps(proposal,indent=2)+'\n',encoding='utf-8')
print('Candidate profile unions measured cargo movement/actions/actual life cargo-turn gate with existing bounds; runtime unchanged.')
