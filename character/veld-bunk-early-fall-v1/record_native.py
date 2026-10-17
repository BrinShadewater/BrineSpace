from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-bunk-early-fall-native-v1';G=R/'output/veld-bunk-body-settle-v1'
report=json.loads((O/'validation.json').read_text());regression=json.loads((G/'validation.json').read_text())
assert report['passed'] and regression['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==8
captures=len(list(O.glob('*-room.png')))
old=json.loads((P/'candidate-evidence.json').read_text())['bindings']
assert all(old[f.relative_to(R).as_posix()]==hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'frames').rglob('*.png'))
note=f'''## Veld early bunk floor-fall native integration - October 1, 2026

Explicit earlyBunkFloorDeathMode=floor-v1 marks only standing/crouching floor
families in CrewSpritePlayer. Veld selector requires matching gear, active dry
bunk entry/exit, source pose0/1, matching canonical first pixels and opt-in tag.
Seated/reclining pose2+ still uses supported settling. Strict saved recipe
requires exact early source index/gear, first1 and zero lifted position; foreign
bed anchors, later poses, shifted roots and mismatched equipment reject.
Exact180ms incoming whole pose/depth retained, then original floor-root clip
timing/depth and canonical resting terminal. No source repaint/rescale this
interval.105package checks now107 with two explicit opt-in assertions;35builder
checks retain their source scope. All22PNGs match earlier artwork milestone.

Native21094checks0fail/{report['seconds']}s, engine terminal0/clean log. Eight
actual RoomFlooding.kill cases: early standing/crouch lowering and rising,
both gears. Eight ordinary eligible full disk checkpoint writes/reads and fresh
main-scene restore_staged operations,2400future20ms actor steps total. Independently
assert authored frame clock, floor offsetzero, stationary physical foot and exact
canonical floor terminal; compare every uninterrupted/restored source hash,
clock/timer, needs, pose/state/gear/dead, position/depth.32malformed recipe guards.
Existing Bill ward paid/restored in fixture and wakes through actual recovery/
roster to preserve normal run eligibility; no run resurrection/freebuild bypass.
{captures}actual room captures plus{captures}exact source PNGs; eight paired boards
reviewed against original-scale standing masters. Visible floor contact in front
of bunk, attached anatomy, matte palette and helmet preserved after Continue.

Scoped regressions native14813partial source/API checks/80cases/320same-clock
actor-file restores across four room rotations; native1306held/live checks and
headless1953water checks/64oxygen deaths all pass. Three engines terminal0/clean
logs,{regression['seconds']}s. Both intervals use scratch APPDATA; owner
{report['realProfileFileCount']}non-log files unchanged.53targeted early interval
inputs and29targeted regression inputs before/after match; broader dependencies
not frozen. New test/UID and runner, original source and detailed native evidence
retained. Normal paired library remains staged/unselected; no commit/export.

Lesson: early floor falls need pose/gear-bound opt-in selectors and zero furniture
lift, while supported deaths need saved dynamic bed anchors. Validate both source
clock and actual room contact, then eligible full checkpoint/fresh scene future
motion. Exact source continuity does not prove floor placement on its own. Keep
prescribed rotation-zero early phase/world mortality API and actor-only future
updates distinct from natural whole-world hazards, title/new process Continue
and every-room visual acceptance. Lounge fall sources, whole-world cadence,
normal paired body installation and full Veld/master cross-family polish remain
open. Full goal active/incomplete; owner visual acceptance open.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
 old_bytes=path.read_bytes();payload=note.replace('\n','\r\n').encode()
 if note.splitlines()[0].encode() not in old_bytes:path.write_bytes(payload+b'\r\n'+old_bytes if i==0 else old_bytes+b'\r\n'+payload)
handoff=f'''# Project handoff

Updated:2026-10-01 - Project:BrineSpace - Task:Veld early floor-fall integration

## Objective and acceptance
Full Veld master-matching animation set, then cross-family consistency/polish.
Goal active/incomplete. Paired early floor falls staged; owner acceptance open.
No normal paired library selection, commit or export.

## Accepted decisions and constraints
Selected East master identity/physique/matte grade; one148/495 source ruler.
256x272/p128,224/H148. Exact existing crouch entry and ground terminal, master
native helmet.22PNGs unchanged. Preserve owner rooms and real profile.

## Current state
Raw source/prompt/builders/manifests/reviews retained here. Production loader
opt-in early floor tags; strict dry early-pose selector/recipe validator in
veld_death_motion.gd. Only bunk poses0/1 use floor family,2+ retains supported
settling. Test_veld_bunk_early_fall_native.gd/UID, isolated runner and8boards.

## Verification
35source/107package checks;21094native checks0fail/{report['seconds']}s,
8actual world kill API cases/8fresh eligible disk Continue restores/2400future
actor steps;{captures}room+source captures,8boards/master comparisons reviewed.
Independent authored clock/zero floor lift/exact terminal plus uninterrupted
versus restored source/contact/depth.32invalid recipe guards. Existing Bill
recovery keeps run eligible. Native14813partial/1306held and headless1953water
regression checks0fail/{regression['seconds']}s. All engine0/clean logs; owner
{report['realProfileFileCount']}non-log files unchanged,53/29targeted inputs frozen.
Normal paired body unselected; prescribed early rotation-zero phases and
actor-only future updates do not prove natural whole-world hazard cadence,
title/fresh-process Continue or universal room/owner acceptance.
Prior complete-body bunk lifecycle/approach/fire/partial/held/water evidence
stays in character/veld-bunk-body-master-v1 with dated scoped reports.

## Next action
Lounge fall sources/transition coverage, then whole-world hazard cadence and
normal paired bunk body installation. Finish remaining Veld families and
full-set master/cross-family polish. Full goal remains active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[O/n for n in ['native.log','records.json','validation.json','inputs-before.json','inputs-after.json']]+[G/n for n in ['validation.json','native.log','held-regression.log','water-regression.log','inputs-before.json','inputs-after.json']]+[R/'scripts/crew_sprite_player.gd',R/'scripts/veld_death_motion.gd',R/'tests/test_veld_bunk_early_fall_native.gd',R/'tests/test_veld_bunk_early_fall_native.gd.uid',R/'tools/run_veld_bunk_early_fall_native.py']+list(P.glob('native-floor-*.png'))+[P/'native-review.html',P/'review_native.py',P/'record_native.py',P/'bare-manifest.json',P/'helmet-manifest.json',P/'package-checks.json']
(P/'native-evidence.json').write_text(json.dumps({'validation':report,'regressionValidation':regression,'nativeChecks':21094,'freshDiskRestores':8,'futureActorSteps':2400,'nativeRoomCaptures':captures,'exactSourceCaptures':captures,'sourcePNGsEqualArtworkMilestone':True,'normalPairedSelection':False,'visualReview':'Eight paired native/source boards against standing masters, actual floor contact in front of bunk','scope':'Prescribed early phases at rotation zero; actual world mortality API, actor-only future updates; not natural whole-world hazard cadence','bindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n')
index=P/'index.html';link='<p><a href="native-review.html">Actual floor contact and Continue motion comparisons</a></p>';s=index.read_text()
if link not in s:index.write_text(s+'\n'+link,encoding='utf-8')
b=R/'character/veld-bunk-body-master-v1/HANDOFF.md';s=b.read_text(encoding='utf-8')
s=s.replace('integrate strict selectors/native floor contact and mortality/Continue next.','early selectors/native floor contact/8actual deaths and full Continue pass.')
b.write_text(s,encoding='utf-8')
print(f'21094native checks;{captures}captures;three regressions;five notes/handoffs saved')
