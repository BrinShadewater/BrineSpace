"""Preserve authored shared-pose equality across parent actions and cancellation aliases."""
from pathlib import Path
from PIL import Image
import json,hashlib,copy
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1];SRC=R/'character/krusher-coherent-bank-v2';O=R/'character/krusher-coherent-bank-v3';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());audit=read(H/'alias-audit.json');index=read(SRC/'candidate-bank-index.json');replacements={};records=[]
def rank(q):
 key=q['state'].split(':',1)[1]
 return (not key.startswith(('idle-','walk-','interact-')),any(part in key for part in ['return-','cancel-','release-']),key.startswith('meal-'),len(key),q['frame'],key)
for conflict in audit['conflicts']:
 candidates=[q for variant in conflict['variants'] for q in variant];best=min(candidates,key=rank);target=R/best['file'];donor=np.array(Image.open(target).convert('RGBA'))
 for q in candidates:
  if q['file']==best['file']:continue
  source=R/q['file'];a=np.array(Image.open(source).convert('RGBA'));assert a.shape==donor.shape
  if np.array_equal(a,donor):continue
  old=replacements.get(q['file']);assert old is None or old==best['file']
  replacements[q['file']]=best['file'];changed=np.any(a!=donor,2);yy,xx=np.where(changed)
  records.append({'state':q['state'],'frame':q['frame'],'source':q['file'],'representativeState':best['state'],'representativeFrame':best['frame'],'output':best['file'],'differentPixels':int(changed.sum()),'differenceBox':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]})
out={'candidatePacks':{'bare':[],'helmet':[]}}
for gear,paths in index['candidatePacks'].items():
 for i,path in enumerate(paths):
  m=read(R/path[6:])
  for s in m['states']:
   s['frameFiles']=['res://'+replacements.get(f.removeprefix('res://'),f.removeprefix('res://')) for f in s['frameFiles']]
  dest=O/'packs'/f'{gear}-{i:02d}.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(m,indent=2)+'\n');out['candidatePacks'][gear].append('res://'+dest.relative_to(R).as_posix())
(O/'candidate-bank-index.json').write_text(json.dumps(out,indent=2)+'\n')
(O/'alias-consolidation.json').write_text(json.dumps({'oldPoseGroups':audit['originalPoseGroups'],'consolidatedGroups':len(audit['conflicts']),'changedSlots':len(records),'method':'Same historical registered RGBA pose must use one current drawing. Canonical controls and parent actions take priority over their return/cancel derivatives. No new art, resampling or clocks.','records':records},indent=2)+'\n')
print(json.dumps({'consolidatedGroups':len(audit['conflicts']),'changedSlots':len(records),'uniqueReplacementFiles':len(replacements)}))
