from pathlib import Path
import hashlib,json
root=Path.cwd();b=root/'character/marsh-retained-gesture-material-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Retain the first attempt as rejected; never label its uninspected full source board as reviewed.
p=b/'east-return05-unselected/selection.json';r=json.loads(p.read_text());r['board']['actuallyInspected']=True;r['assessment']='Rejected for return timing: arms nearly fully lowered, so it relocates the large jump. East05 whole neutral also broadens to34.009vs own32.';p.write_text(json.dumps(r,indent=2)+'\n')
p=b/'east-return06-unselected/selection.json';r=json.loads(p.read_text());r['board']['actuallyInspected']=True;r['assessment']='Whole halfway return figure visually inspected with all6East sequence slots and own idle. Distinct lowering pose improves semantic progression, but cadence/silhouette transition still provisional; no normal admission.';r['apngDecodedExactFrames']=6;r['apngSha256']=sha(p.parent/'gesture.apng');r['apngTotalDurationMs']=900;r['transitionMetricSha256']=sha(p.parent/'transition-metrics.json');p.write_text(json.dumps(r,indent=2)+'\n')
p=b/'cardinal03-unselected/verification.json';r=json.loads(p.read_text())
for board in r['nativeEvidence']['boards']:board['actuallyInspected']=True
r['visualAssessment']={'scope':'East return06 mixed whole-source comparison and full6pose native board inspected at source/station height. Other directions unchanged, prior native receipts reused.','finding':'Clear intermediate lowering pose; fixed-band silhouette changes375/248 vs prior254/225 on final joins do not prove smoother cadence. Further motion review needed; cardinal03 is a comparison candidate, cardinal02 remains prior staged baseline.','normalAdmission':False,'fullGoalComplete':False}
r['unchangedDirectionsNativeEvidence']={'path':'character/marsh-retained-gesture-material-v1/cardinal01-unselected/verification.json','sha256':sha(b/'cardinal01-unselected/verification.json'),'directions':['west','north','south']}
p.write_text(json.dumps(r,indent=2)+'\n')
receipts=[]
for p in sorted((b/'sources').glob('*.request.json')):
 r=json.loads(p.read_text())
 for ref in r['references']:assert sha(root/ref['path'])==ref['sha256']
 assert sha(root/r['result']['path'])==r['result']['sha256']
 receipts.append({'request':p.relative_to(root).as_posix(),'sha256':sha(p),'result':r['result']})
assert len(receipts)==14
(b/'cardinal03-unselected/generation-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
note='''
## Marsh East halfway return06 candidate — October3,2026

Two whole-source return-pose edits preserved as East05/East06 with exact prompts,
references, IDs and raw SHA receipts (14total retained generations). East05 lowered
arms almost fully: rejected for relocating the discontinuity, also neutral34.009
vs own32. East06 makes a distinct waist-height diagonal forearm pose; all5body
heights661, ONE147/661factor. New neutral33.803vs32 is not preferred over East04.

East-return06-unselected keeps the first3East04 whole gestures and both exact own
idle endpoints, using ONLY East06's whole fourth figure. Each source strip retains
its neutral-derived common density, no per-pose fitting or anatomy/head splice.
Original six150ms finite timing unchanged. Six APNG frames decode exact (900ms).
cardinal03-unselected combines this candidate with unchanged West03/North02/South03.
It is a comparison candidate; cardinal02 remains prior staged baseline, no normal
catalogue change or actual helmet behavior enabled.

Rejected East05 and candidate East06 six-slot source comparisons actually viewed.
Candidate native full6pose board inspected at source and station65.28height.
East-only192checks/52samples/6player restores/6captures,0errors/warnings/failures,
exit0;1067bounded inputs and2931owner non-log files unchanged under scratchAPPDATA.
Unchanged directions reuse prior cardinal01 native receipts, not a new complete run.

Lesson: a near-idle frame can merely relocate a jump; specify a genuine intermediate
with hands between held and relaxed positions, then inspect the whole sequence.
Connected source/material/identity and exact finite timing do not prove cadence.
Fixed alpha>80 band rows58..121 adjacent changed pixels on final joins are375/248
for candidate vs254/225prior; this includes body edges/registration, is not tracked
hand distance, and DOES NOT establish improved smoothness. Distinct semantic pose
is provisional until timed motion/body/hand continuity review; don't claim success
from generation prompt or green player tests. Need review before selecting candidate,
then analogous West/North/South return poses, coherent admission and remaining
full-family/controller/consistency polish. Full goal stays active.
'''
canonical=root/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [root/'character/ANIMATION_PIPELINE.md',root/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',root/'docs/CURRENT_STATUS.md',canonical]:
 with p.open('rb') as f:f.seek(max(0,p.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
 if '## Marsh East halfway return06 candidate' not in tail:
  with p.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('14generation receipts/source-native reviews, limitations and skill/pipeline/bible/status updates recorded')
