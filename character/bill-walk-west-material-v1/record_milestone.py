from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-walk-west-material-selected-native-v1'
assert not (P/'runtime-evidence.json').exists()
n=json.loads((O/'validation.json').read_text());v=json.loads((P/'verification.json').read_text());log=(O/'native.log').read_text();assert n['artPassed'] and n['returnCode']==0 and '442 checks,0 failures' in log and v['checks']==536
files=[P/'manifest.json',P/'helmet-manifest.json',P/'material-registration.json',R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json',R/'tests/test_bill_walk_west_material_selected.gd',O/'native.log',O/'loaded-water-carry.png']
(P/'runtime-evidence.json').write_text(json.dumps({'packageChecks':536,'nativeChecks':442,'nativeFailures':0,'native':n,'sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'scope':'Paired48-pose west walk material/head correction; original gait, bounded protected source, complete crown and equipment-specific pixels. Normal-loader source/phase and bare distance evidence; no live route/Continue or owner acceptance','fullGoalComplete':False},indent=2)+'\n')
note='''

### Bill paired west walk native identity and restrained fabric chroma — October 1, 2026
Selected bill-walk-west-material-v1 has48 bare+48 equipped west walking poses. Rejected broad hair/fabric gain mixed face shadows into hair and failed visual color matching; retained initial comparison/recipe under review-rejected-v1. Final bare head is exact native accepted west master pixels, scale1, with complete gray crown coverage. Earlier warm-only head segmentation omitted four crown rows even though every retained pixel matched the master and silhouette connectivity passed. Subset pixel equality is insufficient: separately prove full crown coverage, including gray hair and low-alpha edges. Horizontal fitting must use the actual directional master crown axis, not generic canvas128. Completed west walking crown14 width20 throughout matches master20; width remains diagnostic, not full anatomy acceptance.
Fabric pass targets only magenta gray pixels, fixed75% blend toward one pooled master collar chroma, renormalized to original pixel luminance. No per-pose gain or anatomy resampling; alpha/details/pixels outside the bounded material/head region preserved. Quantized fabric luminance change max.4738/255. Gear-specific pixels, including helmet hardware/face, exactly unchanged; equipment only grades body pixels exactly shared with bare original. Whole canvas translation to256/p128,224/H148; original48-phase2s/.1796875cell gait retained.
536 package +442 normal-loader native checks pass, engine0/12.69s. All bare phases exact loaded pixels/registration/time+distance clock, equipment all48 exact source/pivot/time; fresh1792x1792 bare all-pose native board and paired source boards reviewed. Prior native failures were stale fixture manifest/master paths; retained in runner interval archives, corrected before successful evidence. Strict2931-file non-log profile guard false,last_session.json only; attribution unproven, no owner restore or retry to clean guard. Literal normal paired overrides/ACTIVE_ASSETS selected; current inventory locomotion-v6 remains212bare/194helmet, source/moving reviews rebuilt. Next audit earlier native head components for complete crown coverage; then remaining material/motion/full-family and physical/service/Continue contexts. Full goal active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Bill west walk material/head consistency

## Objective and acceptance
Continue full Bill set and cross-family master/material/anatomy/perspective/motion polish. Previous goal turn was progress:30 north walk poses selected with404 scoped checks. This milestone selects96 paired west walk poses; full goal and owner visual acceptance remain open.

## Accepted decisions and constraints
Native master proportions/matte finish; original2s/.1796875cell walking gait. Exact native bare head, no part resampling. Fixed luminance-preserving fabric chroma only where magenta; gear-specific pixels remain exact. No gameplay heading/run behavior, owner-save restore, export/commit/push.

## Current state
Paired manifests,96 frames, native complete master head, material/head masks and registration in this folder. build.py/verify.py rebuild locally; select_and_prepare.py is one-time and guarded. Normal grid paired literal paths and ACTIVE_ASSETS selected. Fixture tests/test_bill_walk_west_material_selected.gd and UID; scratch runner/native report. Original sources unchanged; rejected gain comparison/recipe retained. Inventory locomotion-v6 and current cardinal sampled/all-frame/moving source reviews rebuilt.

## Verification
536 package checks include complete crown coverage, exact retained master pixels, connected heads, protected body/alpha, fabric luminance rounding, equipment-specific pixels, source hashes and original gait. Native442 checks/0 failures, engine0/12.69s; fresh1792x1792 bare all-pose native capture reviewed, paired source boards reviewed. Earlier fixture-path failures preserved in interval archives. Strict real-profile guard false,last_session.json changed among2931 non-log files; attribution unproven. No actual NPC journey/Continue or whole-set motion acceptance claim.

## Next action
Audit complete crown coverage of earlier run-head components and north walk: warm segmentation may omit gray hair despite exact subset equality. West walking component now fixes that omission independently; do not silently change previous accepted test expectations. Then close-review remaining cardinal walk boards/moving joins, other selected families and prior physical/service/checkpoint gaps. Source-key counts212bare/194helmet do not establish completion.
'''
(P/'HANDOFF.md').write_text(handoff)
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/name).open('ab') as f:f.write(note.encode())
shutil.copy2(R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md'))
status=R/'docs/CURRENT_STATUS.md';prefix='''## Bill paired west walk material and complete crown — October 1, 2026

Selected bill-walk-west-material-v1 fixes purple hair via exact native accepted head and magenta gray fabric via fixed75% master-neutral chroma blend preserving luminance.48 bare+48 helmet frames; helmet-specific pixels unchanged. Complete crown coverage check caught four gray rows omitted by earlier warm-only component segmentation: exact subset equality was insufficient. Corrected west walking crown20 matches master throughout; anatomy/gait remain native,2s/.1796875cell,256/p128,224/H148.536 package+442 normal-loader native checks pass, paired source/all-pose native reviewed; earlier fixture path failures archived. Strict2931-file non-log guard false,last_session.json only, attribution unproven. Source inventory locomotion-v6 remains212bare/194helmet; reviews rebuilt. Next audit earlier run/north-walk components for complete crown coverage, then remaining materials/motion/full-family and physical/service/checkpoint scopes. Full goal active. See character/bill-walk-west-material-v1/HANDOFF.md.

''';status.write_bytes(prefix.encode()+status.read_bytes());print('Recorded paired west walk,978 scoped checks,complete-crown lesson and remaining full-set work')
