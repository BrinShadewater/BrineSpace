from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-walk-north-master-head-selected-native-v1'
assert not (P/'runtime-evidence.json').exists()
n=json.loads((O/'validation.json').read_text());v=json.loads((P/'verification.json').read_text());log=(O/'native.log').read_text();assert n['artPassed'] and n['returnCode']==0 and '280 checks,0 failures' in log and v['checks']==124
files=[P/'manifest.json',P/'head-registration.json',R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json',R/'tests/test_bill_walk_north_master_head_selected.gd',O/'native.log',O/'loaded-water-carry.png']
(P/'runtime-evidence.json').write_text(json.dumps({'packagingChecks':124,'nativeChecks':280,'nativeFailures':0,'native':n,'sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'scope':'Selected30-pose north bare walk native-head fit; protected original body/source clock/stride and unchanged equipment selection. Source/native captures reviewed; full motion, live routes/Continue and owner acceptance remain separate','fullGoalComplete':False},indent=2)+'\n')
note='''

### Bill all-frame walking review and north native-head fit — October 1, 2026
Added build_all_walk_review.py in bill-locomotion-consistency-audit-v2: every selected cardinal walk pose in both profiles,370 frame presentations plus8 native master references, common native148/82 density and head/neck crops. Source manifest hashes and loader snapshot checked. Crown14 width is a diagnostic, not an anatomical acceptance metric. North bare walking crown20..21 versus master18 was visibly broader and green-tinted; west hair/collar has a purple cast warranting the next material pass. North/west bare full-frame boards reviewed; other built boards still require close visual review.
Selected bill-walk-north-master-head-v1 now fits the exact22x25 accepted native rear-head component to all30 original walking bodies, scale1; no new body pose, gait timing, stride or per-pose color normalization. Whole original184 canvas translated36,52 to256 with paired foot pivot128,224/H148; every body pixel outside bounded head/erase region remains exact. Source gait30x50ms/1.5s/.1796875cell retained. Existing30 helmet frames/canvas/pivot/clock stay at their independent normal selection. Crown width now18 throughout, all30 have one substantial alpha160 component; physical connectivity does not prove natural shoulder motion.
124 package and280 normal-loader native checks passed, engine0/13.8s; all-pose1536x1536 native board reviewed. Strict2931-file non-log profile guard false,last_session.json only; attribution unproven, no restore or guard-clean retry. Whole literal normal bare override and ACTIVE_ASSETS updated; paired fixture UID retained. Inventory locomotion-v5 remains212bare/194helmet; sampled cardinal and authored-clock join reviews rebuilt against current selection. Further west/other material consistency, all-direction moving joins, broader full-family anatomy/perspective and physical/service/checkpoint contexts remain; full goal active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Bill north walk master-head consistency

## Objective and acceptance
Continue complete Bill animation/master consistency and full-set polish. Previous goal turn was progress:24 corrected run poses selected,426 scoped checks. This milestone adds a30-pose walking head correction and stronger all-frame walk evidence. Full goal and owner visual acceptance remain open.

## Accepted decisions and constraints
Keep native master proportions/matte colors, independently authored walking body and original1.5s/.1796875cell gait. Native head component reuse only; do not infer acceptance from width or alpha alone. Existing equipment selection unchanged. No gameplay heading/run behavior, owner-save restore, export/commit/push.

## Current state
30 selected bare north walk frames, native22x25 head, bounded source erase masks and registration in this folder. build.py/verify.py rebuild locally. Normal grid literal manifest and ACTIVE_ASSETS override updated. Fixture tests/test_bill_walk_north_master_head_selected.gd with paired UID and scratch runner. All-cardinal walk review builder/8 boards/json in bill-locomotion-consistency-audit-v2; new dated locomotion-v5 source inventory and current sampled/moving reviews rebuilt.

## Verification
124 package checks: exact native master head, source clock/stride, original source hashes and protected body after whole-canvas translation, all30 connected at alpha160. Native normal-loader280 checks/0 failures, engine0/13.8s: every bare/gear source, phase/density/pivot, bare distance clock/wrap/stationary and fresh all-pose native capture, reviewed. Strict real-profile guard false,last_session.json changed among2931 non-log files; attribution unproven. No actual NPC journey/Continue or broad motion acceptance claim.

## Next action
Close-review remaining cardinal full-frame walk boards and moving joins. West bare hair/collar purple cast is the next evidenced material mismatch; choose a shared source/material transform and compare with master and equipment, preserving alpha, anatomy, detail and gait. Then other selected families/full motion and previously unproven physical/service/checkpoint contexts. Source counts212bare/194helmet do not establish full fidelity.
'''
(P/'HANDOFF.md').write_text(handoff)
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/name).open('ab') as f:f.write(note.encode())
shutil.copy2(R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md'))
status=R/'docs/CURRENT_STATUS.md';prefix='''## Bill north walk native master-head consistency — October 1, 2026

All-frame cardinal walk review built370 pose presentations in both profiles. North bare head was broader/green-tinted; selected bill-walk-north-master-head-v1 now uses exact native22x25 rear head across30 original bodies, preserving original gait1.5s/.1796875cell and protected source body pixels. Whole184->256 canvas translation only,p128,224/H148. Existing helmet30 frames/registration unchanged.124 package +280 normal-loader native checks pass; all-pose native board reviewed. Strict2931-file non-log guard false,last_session.json only, attribution unproven. No whole-route/Continue or owner acceptance claim. Current inventory locomotion-v5 remains212bare/194helmet; reviews rebuilt. Next evidenced mismatch: west walk hair/collar purple cast; remaining boards/moving joins/full-family and prior physical/service/checkpoint contexts stay open. Full goal active. See character/bill-walk-north-master-head-v1/HANDOFF.md.

''';status.write_bytes(prefix.encode()+status.read_bytes())
print('Recorded north walk selection,404 scoped checks,all-frame walk diagnostic and continued material pass')
