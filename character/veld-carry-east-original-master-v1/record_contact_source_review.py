"""Record independent source gates without mutating frozen native evidence."""
from pathlib import Path
import json, shutil, uuid, time, hashlib
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent; R=P.parents[1]
items=[('prelift-source-v1','49343055-3798-4ceb-8613-c44a51788457','raw-prelift-v1.png','Rejected requested prelift: far boot already clearly airborne; insufficiently distinct from retained lifted-foot key.'),('touchdown-source-v1','cbac3b06-8895-4638-9331-de0377e99f8e','raw-touchdown-v1.png','Rejected requested touchdown: forward far heel remains airborne, head28 exceeds original26-27 range; upper body45 vs42.')]
ledger=json.loads((P/'EXECUTIONS.json').read_text(encoding='utf-8'))
for folder,identifier,raw,verdict in items:
 s=P/folder; audit=json.loads((s/'source-audit.json').read_text(encoding='utf-8'))
 a=np.array(Image.open(s/'transition-candidate.png').convert('RGBA'))
 # Spatial footprint diagnostic only, not semantic heel or physical-contact proof.
 ys,xs=np.where(a[200:,:,3]>200); right=xs>=143
 diagnostic={'rightFootRegionXMin':143,'opaqueBottom':int(ys[right].max()+200),'wholeFigureFloor':audit['rows'][1]['floor'],'scope':'Screen-right boot opaque extent, not a calibrated physical heel landmark.'}
 entry={'id':identifier,'folder':folder,'raw':folder+'/'+raw,'prompt':folder+'/prompt.txt','references':['../veld-east-held-original-master-v1/raw-held-v1.png','single-transition-source-v1/raw-transition-v1.png'],'status':'Completed; rejected requested motion state','verdict':verdict,'sourceAudit':audit,'footExtentDiagnostic':diagnostic,'visualReview':'Complete same-scale master/source comparison plus enlarged heads and legs inspected. No native packaging/adoption for rejected state.','bindings':{n:hashlib.sha256((s/n).read_bytes()).hexdigest() for n in [raw,'prompt.txt','source-audit.json','transition-candidate.png','source-master-review.png']}}
 (s/'VERDICT.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf-8')
 if not any(g['id']==identifier for g in ledger['generations']): ledger['generations'].append(entry)
(P/'EXECUTIONS.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
title='## Veld East contact-source semantic gate — October 3, 2026'
note=title+'''\n\nTwo independent whole-pose sources saved with exact prompts/raw/audits:
prelift49343055-3798-4ceb-8613-c44a51788457 and touchdowncbac3b06-8895-4638-9331-de0377e99f8e.
Both use original held appearance plus retained lifted-foot motion guide. Full
same-scale comparisons and enlarged heads/legs inspected. Prelift148/head26/
upperbody44/cloth68,66,66; touchdown148/head28/upperbody45/cloth66,65,64 versus
held148/head26/upperbody42/cloth66,64,63 and original empty head27.
No clipping. Appearance measures do not certify requested movement: prelift far
boot is already airborne; touchdown far heel still floats. Both REJECTED as
requested states, preserved with hashes/verdicts; no native/package/adoption.

Lesson: explicitly verify motion semantics separately from master-height/colour
checks. A lifted-foot reference can anchor a new source to the wrong phase even
when wording asks for earlier prelift or heel contact. Next conditioning removes
that guide and uses only original master, specifying same-floor double support.
Never lower or reconstruct a boot procedurally to manufacture contact evidence.
Current successful one-key source and fixed video/native records untouched.
Next actual heel-contact source, complete start/stop and moving foot/root joins;
East full support/near-far identity, North gait, full original action/direction,
furniture, ordinary controllers/save/Continue and final library polish remain.
Full goal active/incomplete. Handoff: character/veld-carry-east-original-master-v1/HANDOFF.md.
\n'''
h=P/'HANDOFF.md'
if title not in h.read_text(encoding='utf-8'):
 with h.open('a',encoding='utf-8') as f:f.write('\n'+note)
template=(P/'record_native_milestone.py').read_text(encoding='utf-8')
exec(compile(template[template.index('paths=['):],str(Path(__file__)),'exec'))
print('Recorded two rejected motion states; master-guided contact conditioning changed.')
