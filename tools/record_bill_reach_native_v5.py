"""Bind inspected current native evidence and cross-family findings."""
from pathlib import Path
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-reach-adjacent-motion-v2';N=P/'native';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((N/'validation.json').read_text(encoding='utf-8'));assert v['passed'] and v['checks']==910 and v['failures']==0
frozen=json.loads((N/'inputs-before.json').read_text(encoding='utf-8'));assert all(sha(Path(p))==h for p,h in frozen.items())
family=json.loads((P/'family-review.json').read_text(encoding='utf-8'));assert all(sha(Path(p))==h for p,h in family['inputs'].items())
native=json.loads((N/'verification.json').read_text(encoding='utf-8'));native.update(nativePagesReviewed=True,visualFindings='All three fixed station crop pages inspected. Current idle/reach visible, matte detail and warmer face survive station density; strict floor alignment stable. Reduced crown variation persists but face/collar and arm arc remain provisional.',pageHashes={name:sha(P/name) for name in native['pages']},fullVisualAcceptance=False)
(N/'verification.json').write_text(json.dumps(native,indent=2)+'\n',encoding='utf-8')
family.update(nativeTested=True,nativeRun='native/verification.json',nativeChecks=910,worldSoleDepthAccepted=True,fullVisualAcceptance=False);family['openIssues']=['One-pixel crown/stature variation and face/shoulder/arm arc remain provisional.','NativeV5 prescribed bare-room source/depth only; natural dispatch, gear, continuous cadence, fullSave/TitleContinue and normal admission remain unverified.'];(P/'family-review.json').write_text(json.dumps(family,indent=2)+'\n',encoding='utf-8')
cross=json.loads((P/'master-cross-family.json').read_text(encoding='utf-8'));assert all(sha(R/p)==h for p,h in cross['inputs'].items());cross.update(status='reviewed_open_consistency_findings',visualReviewed=True,findings=['Staged idle closer to original warm face/quilt; reach face/collar still changes slightly.','Selected idle/walk/run/carry/weld faces generally darker; walking/running fabric smoother and less master detail.','Carry context correctly uses inherited current East gait-v3, not older literal cargo source.','Representative source comparison does not certify all sequences or equipment.'],comparisonSha256=sha(P/'master-cross-family.png'));(P/'master-cross-family.json').write_text(json.dumps(cross,indent=2)+'\n',encoding='utf-8')
for name in ['prepare_bill_east_master_world_v5.py','run_bill_east_master_world_v5.py','publish_bill_east_reach_adjacent_motion_v2.py','build_bill_east_reach_cross_family_v2.py','record_bill_reach_native_v5.py']:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
assert all((R/'tools'/f'{name}.gd.uid').is_file() for name in ['review_bill_east_master_world_v5','ensure_bill_east_master_world_v5_uids'])
pngs=list(N.rglob('*.png'))+[P/'master-cross-family.png'];r=subprocess.run(['git','check-attr','filter','--']+[p.relative_to(R).as_posix() for p in pngs],cwd=R,text=True,capture_output=True,check=True);assert len(r.stdout.splitlines())==len(pngs) and all(x.endswith(': filter: lfs') for x in r.stdout.splitlines())
note='''

## Bill East current reach actual-room and cross-family milestone — October 3, 2026

V5 actual main/Bill/furnished Cold Store bare-room fixture loads current
bill-east-reach-adjacent-motion-v2, binds real retained source tables and checks
all six occupied heights against inspected148/148/149/149/149/148.910checks0,
150prescribed paused source samples,36native/source capture pairs,zero Ysole
findings;engine0/51.07s.4542tested input hashes and2931owner non-log hashes
unchanged,scratchAPPDATA. All4542as-tested inputs and nine source-lineage hashes
rechecked before later review metadata. Native as-tested family report retained.
All three full fixed native crop pages inspected; improved matte detail/warm
face and reduced stature drift persist at station scale. One-pixel stature and
small face/collar variation, abrupt reach return remain open. This is prescribed
bare source/depth evidence, not continuous cadence,2Dplanted feet,natural chooser,
gear/water,fullSave/TitleContinue or normal admission.

Eight representative original-master/staged-idle/reach and selected idle/walk/
run/carry/weld sources compared at common declaredH148/p160224. All figures and
head diagnostics reviewed; whole figures authoritative. Literal plus inherited
closure bindings and current loader block unchanged. Carry uses current East
gait-v3, correcting historical literal cargo context. Selected faces darker and
walking/running fabric smoother/less detailed than master; broad family matching
still open. Never propagate improved single family as full library acceptance.

Five Python syntax checks,two paired native UID files,76new native/cross PNG LFS
attributes verified. Normal source/loader unchanged. Next current reach arc/face
polish plus full East walking master pilot; West48phase/cardinal/gear/water/life/
hazard/fullset consistency remain. Full goal active/incomplete; previous turn
classified progress (complete revised reach bank/source and browser evidence).
Handoff:character/bill-east-reach-adjacent-motion-v2/HANDOFF.md.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for p in paths:
 with p.open('a',encoding='utf-8') as f:f.write(note)
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\nCurrent-source native V5 now passes910checks0/150samples/36capturepairs; allthreepages inspected,4542inputs/2931owner unchanged, scratch. Scope excludes continuous/native natural behavior/fullsave. master-cross-family.json confirms darker/coarser selected gait context, current inherited carry-v3. Source/pose polish remains open. New walking whole-pose master pilot running as functions cell640; preserve terminal raw and compare full geometry before expansion.\n')
print(f'Recorded910check native scope and reviewed cross-family findings;5AST/2UIDpairs/{len(pngs)}PNG LFS; eight maintained records updated.')
