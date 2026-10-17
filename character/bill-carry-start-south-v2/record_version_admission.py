"""Record final South selection evidence without overwriting earlier staged evidence."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
prior=json.loads((P/'input-hashes.json').read_text(encoding='utf-8'))
hashes={k:hashlib.sha256((R/k).read_bytes()).hexdigest() for k in prior}
changes=[k for k in prior if hashes[k]!=prior[k]]
assert set(changes)<= {'scripts/bill_carry_player.gd','scripts/crew_sprite_player.gd','tests/test_bill_carry_normal_snapshot_v1.gd'},changes
outputs=['bill-carry-source-versions-v2','bill-carry-normal-snapshot-v1','bill-carry-south-version-continue-v1','bill-carry-south-version-priority-v1','bill-carry-normal-regressions-v1']
validation={}
for name in outputs:
 v=json.loads((R/'output'/name/'validation.json').read_text(encoding='utf-8'))
 assert v['passed'] and v['returnCode']==0 and not v['realProfileChanges']
 validation[name]=v
for k in ['tests/test_bill_carry_source_versions_v2.gd','tests/test_bill_carry_south_version_continue_v1.gd','tests/test_bill_carry_south_version_priority_v1.gd','tools/run_bill_carry_source_versions_v2_validation.py','tools/run_bill_carry_south_version_continue_v1_validation.py','tools/run_bill_carry_south_version_priority_v1_validation.py']:
 hashes[k]=hashlib.sha256((R/k).read_bytes()).hexdigest()
(P/'version-input-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
evidence={'normalSelectionChanged':True,'sourceVersionPolicy':'New sessions use South gait3/start2 and North gait2/start2. Retained original North/South and revised-North/original-South banks remain available for resumed sessions. No mid-pose migration.','validation':validation,'priorInputChanges':changes,'inputFreeze':'Post-run snapshot; no prelaunch freeze claim. Prior recorded art/manifests unchanged.','visualReview':'Agent reviewed all12 native before/after comparisons, both gears/all3 versions, first step and settlement. Captured size, head/helmet, matte material and pose continuity retained. Static review does not certify continuous contact or loop smoothness.','scope':'Actual selected main/controller/player, actual workshop service with prescribed clear South lane. Twelve disk/fresh-main restores, immediate source/root/clock/pause and30future ticks. Eighteen entry/settlement/North-rise fire/gear/death cases. Fire dispatch/cancellation does not prove completed evacuation. Normal save/Title and bunk regressions pass.','remaining':['Natural short routes and world contact','Continuous loop and cross-family polish','Interrupted carry return and floor crate disposition','Remaining equipment/action coverage and full-set acceptance']}
(P/'version-runtime-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
section='''## Bill South carrying selected with three saved source banks — October 2, 2026

Normal new sessions now use South gait3/start2 with North gait2/start2. The loader
retains complete paired North/South banks for original sources, revised North with
original South, and revised North/South. Restore keeps the saved bank for the
session; incomplete banks and actor/player version mismatches reject before live
mutation. No raster, master, material, room geometry or gameplay rule changes.

3201 source-version guards and604 normal snapshot guards pass.1036native checks/
12fresh disk/main restores pass: all3versions, both gears, South entry/settlement,
exact source/root/clock/pause and30future ticks. All12native before/after pairs
reviewed at station scale;48original captures retained. Captured head/helmet,
proportions and matte appearance remain coherent. Static pairs do not certify
continuous gait/contact.500native priority checks/18cases pass through actual fire
dispatch, public gear change and mortality at entry/settlement/North rise, with
15future cancellation ticks. Fire dispatch is not completed refuge arrival.
Normal save/Title Continue and bunk regression passes. Engine0; all2931owner
non-log files unchanged in every scratch-profile interval. Real workshop service
uses a prescribed clear South lane; no natural chooser/short-route claim.

Source guards6.33s, current shared-player rerun6.42s; snapshot6.47s;
Continue476.61s; priority57.64s; regressions125.89s.
Prior source snapshot differs in selected player, snapshot fixture and concurrent
shared-player Marsh gait-group opt-in. Current3201source guards rerun after shared
change; native results precede it. Recorded art/manifests unchanged. New hashes
are post-run, not prelaunch-frozen.
Full Bill objective active/incomplete. Next natural short-route/contact review,
interrupted carry return/floor crate disposition, remaining equipment/actions and
full cross-family motion polish. No commit/export or owner final acceptance.
Handoff: character/bill-carry-start-south-v2/VERSION_ADMISSION_HANDOFF.md.

'''
status=R/'docs/CURRENT_STATUS.md';s=status.read_text(encoding='utf-8')
if section.splitlines()[0] not in s:status.write_text(section+s,encoding='utf-8')
cont=R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md';s=cont.read_text(encoding='utf-8')
if section.splitlines()[0] not in s:cont.write_text(section+s,encoding='utf-8')
lesson='''
## Paired cardinal source-bank admission — October 2, 2026

When a second direction changes, retain each supported full combination of source
versions. North-only and South-only restoration can silently mix generations.
Cache complete paired North/South frames and clocks, clear target keys before
applying a bank, validate the detached loaded bank, then bind actor and playback
to the same version. Resumed sessions keep their bank; no mid-pose migration.
Verify each combination/direction/gear/source slot, incomplete-bank rejection and
real disk/fresh-main future playback. Record native pose review separately from
static pixel equality and continuous contact. Bill South admission:3201source,
604snapshot,1036native/12restores,500priority/18cases; normal save/bunk passes.
All12 native pairs reviewed; prescribed clear lane, not natural-route coverage.
Evidence: character/bill-carry-start-south-v2/VERSION_ADMISSION_HANDOFF.md.
'''
for file in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 s=file.read_text(encoding='utf-8')
 if lesson.splitlines()[1] not in s:file.write_text(s+lesson,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill South normal admission

## Objective and acceptance
Complete Bill's full master-matched animation set, then full cross-family polish.
This milestone admits revised South carrying; full objective remains incomplete.

## Accepted decisions and constraints
Preserve original masters, matte grade, physical registration and owner geometry.
New sessions use South3/start2 + North2/start2. Three supported full source banks
remain bound for resumed sessions. Tests use scratch APPDATA; no commit/export.

## Current state
Changed scripts/bill_carry_player.gd and missing-bank snapshot fixture. Added
source_versions_v2, South version Continue and priority tests/runners with UIDs.
Native comparison page: version-continue.html;48unmodified captures retained.
Updated current status, continuation, pipeline, bible and both skill references.
Previous HANDOFF.md remains historical staged-source evidence.

## Verification
3201source/604snapshot/1036native Continue/500native priority checks, all0fail.
12fresh restores across3banks/both gears/entry/settlement;18priority cases.
Normal save/Title and bunk regressions pass. Every interval engine0 and2931owner
non-log files unchanged. All12native pairs visually reviewed: captured pose,
proportions and matte head/helmet coherent. Prescribed actual-workshop South lane;
not natural routes or continuous contact. Version-runtime-evidence.json records
reports; version-input-hashes.json is post-run. Prior art/manifests unchanged.

## Next action
Audit actual generated short carrying routes and contact. Then complete carry
interruption/put-down/crate-to-idle lifecycle and remaining equipment/actions;
full-library motion, master and material polish remains open.
'''
(P/'VERSION_ADMISSION_HANDOFF.md').write_text(handoff,encoding='utf-8')
old='This is a staged South candidate. Normal gameplay retains the prior South art. Compatible saved-source admission, interruptions, natural routes and broader contact/loop polish remain under review.'
new='New sessions use this South set. Existing saves retain their paired North/South source version. Save/resume and interruptions pass the current station checks; natural routes and broader contact/loop polish remain under review. <a href="version-continue.html" style="color:#adcddd">View station Continue comparisons</a>'
for name in ['index.html','build_review.py']:
 file=P/name;s=file.read_text(encoding='utf-8');assert old in s or new in s,name
 if old in s:file.write_text(s.replace(old,new),encoding='utf-8')
print('South admission milestone recorded; prior source changes:',changes)
