"""Preserve actual browser advancement and sampled visual-review scope."""
from pathlib import Path
import json,hashlib,ast
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-reach-adjacent-motion-v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
t=json.loads((P/'timeline.json').read_text(encoding='utf-8'));assert all(sha(R/p)==h for p,h in t['inputs'].items())
shots=['browser-extension-003.png','browser-recovery-004.png']
report=dict(scope='Normal/quarter browser advancement and sampled extension3/recovery4 views at source2x/H82/H54. Not continuous human-like observation of all frames or native game acceptance.',normal=dict(completed=1,sampled=150,total=150,timeMs=6760,draws=2853),quarter=dict(completed=2,sampled=150,total=150,timeMs=6760,draws=6774),sampledPoses=[3,4],screenshots={name:sha(P/name) for name in shots},timelineSha256=sha(P/'timeline.json'),sourceHashes=t['inputs'],visualReviewed=True,visualFindings='Both sampled poses viewed at all three scales. Floor line stable, matte detail retained, reduced head rise. Extended-to-recovery pose changes remain abrupt and face/collar construction varies slightly; full polish remains.',nativeTested=False,normalAdmission=False)
(P/'browser-motion-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
for tool in ['record_bill_reach_stature_v2.py','record_bill_reach_stature_browser_v2.py']:ast.parse((R/'tools'/tool).read_text(encoding='utf-8'))
note='\nBrowser follow-up: actual v2 normal and quarter runs complete150/150 at6760ms (completed1/2). Sampled extension3/recovery4 screenshots inspected at2x/H82/H54;78source hashes still exact. Advancement and sampled views do not prove continuously watched cadence. Arc still abrupt; face/collar varies slightly. browser-motion-review.json binds screenshots/timeline/source hashes. No current native or normal admission. Two additional record tools syntax checked.\n'
for p in [P/'HANDOFF.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/CURRENT_STATUS.md']:
 with p.open('a',encoding='utf-8') as f:f.write(note)
print('Recorded normal/quarter completion and two sampled views; all78source hashes unchanged; two record tools syntax pass.')
