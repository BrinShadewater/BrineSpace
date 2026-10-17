"""Record scoped normal-loader evidence and the current master-head lesson."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-run-head-locked-selected-native-v1'
assert not (P/'runtime-evidence.json').exists()
n=json.loads((O/'validation.json').read_text());v=json.loads((P/'verification.json').read_text());log=(O/'native.log').read_text()
assert n['artPassed'] and n['returnCode']==0 and '289 checks,0 failures' in log and v['checks']==137
files=[P/'manifest.json',P/'helmet-manifest.json',P/'head-registration.json',R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json',R/'tests/test_bill_run_head_locked_selected.gd',O/'native.log']+[O/(d+'.png') for d in ['east','west','south','north']]
(P/'runtime-evidence.json').write_text(json.dumps({'packageChecks':137,'nativeChecks':289,'nativeFailures':0,'native':n,'scope':'Native accepted head pixels, bounded protected body, unchanged equipped references, all-direction normal-loader pixels/density/timed and movement clocks; no live run route, checkpoint or owner acceptance claim','sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'fullGoalComplete':False},indent=2)+'\n')
note='''

### Bill native master-head cardinal run layer — October 1, 2026
Close head/neck comparison found wider bare running heads than accepted idle in all four directions, despite broadly coherent full-figure materials. Selected bill-run-head-locked-v1 now uses native accepted directional head pixels at scale1 on the24 independently authored run bodies; no anatomical resampling. Protect the gray collar with a per-row warm-silhouette erase mask, include faint old crown edges, and register the lowest opaque master-head row against the original collar baseline. Crown-only alignment produced detached components in6/24; corrected baseline now yields one substantial alpha160 component in all24. Connected alpha is a necessary seam check, not visual anatomy acceptance. Exact original body outside bounded head/component and original24 helmet references/clocks/stride preserved.
137 package plus289 normal-loader native checks pass, engine0/12.52s; all four fresh1792x1024 native boards reviewed at148/82. Strict2931 non-log profile guard fails on last_session.json only; attribution unproven, no restore or retry for a clean guard. Normal grid and ACTIVE_ASSETS select paired whole literal manifests; maintained four directional fixtures assert current layer rather than historical body-only exports. Original sources/historical reports retained; obsolete East-only prototype builder archived and compatibility entry delegates to current four-direction builder. Current source inventory locomotion-v4 remains212bare/194helmet. Moving selected source-clock join review rebuilt against it; no NPC run behavior or checkpoint claim. Further collar/shoulder motion, lean/counter-swing, materials and full-family/physical/service/Continue contexts remain; full goal active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Bill cardinal run master-head consistency

## Objective and acceptance
Continue full Bill master/material/anatomy/perspective/motion consistency. This layer fixes running head identity and size drift; full goal and owner visual acceptance remain open.

## Accepted decisions and constraints
Keep accepted masters, matte finish, native256 plane/p128,224/H148, independent authored gait/body,540ms clock and .168cell directional stride. Native head reuse is a bounded deterministic consistency fit, not new hand-authored anatomy. Helmet source frames unchanged. Normal Bill NPC still walks; no new run route.

## Current state
24 bare frames and four exact native master components in this folder. Paired manifests selected through scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json. Four existing directional tests updated to current manifest/state IDs. New paired all-direction fixture tests/test_bill_run_head_locked_selected.gd with paired UID; scratch runner tools/run_bill_run_head_locked_selected_validation.py. Original run sources remain untouched. build_candidate.py delegates to build.py; obsolete prototype archived. New inventory bill-selected-source-audit-2026-10-01-locomotion-v4 and current locomotion comparison rebuilt. Diagnostic original head board retained in bill-run-head-master-audit-v1.

## Verification
137 package checks pass; master component pixels exact, protected body exact, original source hashes unchanged, gear references/clock exact, all24 connected at alpha160. Normal-loader native289 checks/0 failures/engine0/12.52s with fresh four148/82 boards, all reviewed. Strict real-profile fingerprint guard false: last_session.json changed among2931 non-log files; attribution unproven. No owner restore, unrelated rerun, actual NPC run or Continue proof. Native evidence in output/bill-run-head-locked-selected-native-v1; snapshots/hashes in runtime-evidence.json.

## Next action
Review moving idle/walk/run joins in all directions and finer head/collar/shoulder/counter-swing/material cadence; then other selected families against masters and previously unproven physical/service/Continue contexts. Current source review is bill-locomotion-consistency-audit-v2/join-review.html. Source-key counts212bare/194helmet do not establish completion. No export/commit/push in this milestone.
'''
(P/'HANDOFF.md').write_text(handoff)
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/name).open('ab') as f:f.write(note.encode('utf-8'))
shutil.copy2(R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md'))
status=R/'docs/CURRENT_STATUS.md';prefix='''## Bill cardinal run native master-head consistency — October 1, 2026

Selected bill-run-head-locked-v1 fixes wider bare running heads in all4directions using exact accepted native heads, collar-baseline registration and protected original bodies.24 bare exports;24 equipped frames unchanged references. Paired normal loader/ACTIVE_ASSETS and current direction fixtures updated.137 package +289 normal-loader native checks pass, four148/82 boards reviewed; strict2931-file profile guard false,last_session.json only, attribution unproven. No actual NPC run/Continue or owner visual acceptance claim. Source inventory locomotion-v4 remains212bare/194helmet; moving source joins rebuilt. Full-set identity/material/anatomy/perspective/motion and prior physical/service/checkpoint contexts remain active. See character/bill-run-head-locked-v1/HANDOFF.md and runtime-evidence.json.

''';status.write_bytes(prefix.encode()+status.read_bytes())
print('Recorded master-head selection,426 scoped technical checks and separate failed profile guard')
