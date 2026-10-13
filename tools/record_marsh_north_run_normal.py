"""Append verified North03 normal acceptance and whole-pose repair lessons."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-north-run-material-v1'
MARKER='## Marsh North run03 normal full Continue milestone — October 2, 2026'

def main():
    stage=json.loads((BASE/'actor-review-v2/verification.json').read_text())
    proof=json.loads((BASE/'normal-review-v1/verification.json').read_text())
    assessment=json.loads((BASE/'normal-review-v1/visual-assessment.json').read_text())
    parity=json.loads((BASE/'actor-review-v2/run02-motion-parity.json').read_text())
    assert stage['visualReviewed'] and stage['checks']==444
    assert proof['failures']==0 and proof['fullCheckpoints']==8 and proof['freshVisibleTitleContinues']==8
    assert assessment['allEightPairsInspected'] and assessment['allFacingRunBoardsInspected']
    assert parity['namedMotionFieldsEqual']==475 and parity['changedCompleteSlots']==[4]
    selected=json.loads((BASE/'selection.json').read_text())
    selected.update(status='provisional complete North run03; eight full normal checkpoints/fresh visible Title Continues verified',normalAdmission=True,fullGoalComplete=False,normalReview='normal-review-v1/index.html')
    (BASE/'selection.json').write_text(json.dumps(selected,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_north_run_normal.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift'
    lesson=f'''
{MARKER}

Full Marsh master/style/camera/size/height/proportion/grade goal remains active
and incomplete. North run03 is provisionally selected in the ordered normal body
catalog. Root selection marks normal admission and full eight-checkpoint proof;
historical source/candidate/staged flags retain their original unselected scopes.
No gameplay/controller/economy/failure/navigation/save-schema changes.

Passing04 whole figure exec-93a3e4e6-3c34-4012-99e9-2877ff98db8d corrects
passing03 contact-like arms: both elbows now bent beside waist, correct RIGHT
support with LEFT sole raised. Selected idle first/PRIMARY, complete previous
passing figure second as posture correction guide, own original rear master third.
Exact frozen prompt, ordered reference/source SHAs, raw/original path/ID retained.
One neutral146 BOX scale .1638608305274972 yields passing62x147 and ruler59x147.
Actual sampled147 versus target146 recorded, not forced per-pose fitting. Strong
sole clearance remains provisional; selected idle55x146 versus ruler59x147 is a
profile/body diagnostic, not exact geometry acceptance. Rear hair whorl/plate/
harness/right-temple edge and authentic charcoal soles preserved. Whole source,
selected/ruler comparison and complete cycle inspected. Standard whole alpha128
packing only; no mirror, limb patch, recolour or pose-specific scaling.

Candidate03 replaces ONLY whole slot4 from candidate02. Five other run files are
byte-identical. Complete sizes58x148/57x145/57x140/59x146/62x147/58x132;
184canvas,p92/172,H148,existing six100ms loop and explicit North stride
.11027027027027027 retained. Six decoded APNG frames equal sources; illustrative
holds are not continuous native film. Complete rear body/head/quiet warm grade
closer to the selected idle/master, arm crossing improved. Contact projection,
flight/hip/sole joins remain provisional for full-set moving polish.

Fresh staged actual Marsh.move/main/grid/player follows the validated physical
North negativeY168world route, fixedX, actual direction segment_clear. Fixture
UIDcx5nhrunm8v91 paired. {stage['checks']} checks,8 exact source/native crop views,
{stage['controlledSamples']} controlled20ms samples,{stage['wraps']} wraps,6 actor/
player restores and pause holds,normal walk slowing. Zero failures/engine errors,
exit0;{stage['stableBoundedInputs']} bounded inputs stable and
{stage['unchangedOwnerNonLogFiles']} owner non-log files unchanged in scratch
APPDATA. All eight views in two boards inspected. Compared with run02:475 named
motion fields (elapsed,slot,running,foot,playerPhase) across95 samples and8 capture
roots equal. No framebuffer or articulated contact equality claim.

Independent test_marsh_north_run_production.gd UIDcy6nhrunm9v92 uses normal
Marsh factory/ordered catalog/main/grid/player/full update, no staged manifest
injection or custom movement. Six expected whole quoted res paths, no constructed
art path. Eight full RunSave checkpoints: idle,six phases,slowing walk. Every fresh
actual Title._continue_loop waits observable startup AND real loading Continue
enabled/pressed/overlay gone. Whole actor/player/source/root parity and pause;
each run resumes normal negativeY movement/distance phase after unpause. Restore
retargets scratch run_save_path. Normal free-build/disabled-failure flags false;
dedicated fixture room placed free, not paid-construction proof.

Normal evidence: {proof['checks']} checks,8 full saves,8 fresh visible Continues,
16 captures,8 exact before/continued source pairs,0 failures/engine errors,exit0.
{proof['stableBoundedInputs']} bounded inputs stable,
{proof['unchangedOwnerNonLogFiles']} owner non-log files unchanged. All8 native
pairs and correct east/west/north/south selected idle/run whole board inspected.
Catalog {proof['normalCatalog']['bodyManifests']} body manifests/228 states/1190
slots is coverage only. Test registered companions/native900 after launch;
tests/index metadata excluded from the input freeze. No natural traffic,
full-scene occlusion,continuous moving sole contact or equipment/full-family
acceptance. Normal-review-v1/index.html holds the scoped evidence and comparisons.

Lessons: make passing arm crossing explicit independently from a correct support
leg reference. Put the selected body first when an earlier stance reference keeps
carrying an unwanted contact posture into edits. Keep whole source support/camera/
anatomy judgments separate from ruler dimensions and playback tests. Reverse only
the physical route, never asymmetric identity. Verify normal full Continue after
staged acceptance instead of transferring another facing's proof. Preserve all
four comparison directions when adapting a publisher.

Next: master-match carry and remaining held families, then complete full-set
consistency/polish across camera/body/head/equipment/grade and continuous motion.
Current four cardinal runs are provisionally improved and independently normal
checkpoint-verified; this does not complete the full animation set or polish.
Goal remains active/incomplete.
'''
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(lesson)
    installed.write_bytes(maintained.read_bytes())
    handoff=f'''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: North03 normal run

## Objective and acceptance
Full master-matched set/consistency/polish active and incomplete. North03 normally
selected provisionally;8 full checkpoints/fresh visible Title Continues verified.
Passing arms corrected; body/grade joins improved. Continuous contact/flight/sole
polish and full-family/equipment consistency remain.

## Accepted decisions and constraints
Own55x146 rear idle/original master, authentic raised charcoal soles and rear
equipment/right-temple edge. Complete passing04 pose and one neutral scale,
actual sampled147 versus target146 recorded. No mirroring/patch/recolour/pose fit.
184canvas,p92/172,H148,six100ms/current distance cadence. Scratch APPDATA;
owner profile unchanged. Normal economy/failure flags unchanged. Dedicated free
fixture site is not paid-construction proof. No gameplay changes.

## Current state and changed files
New passing04 prepare/build/provenance/whole source/ruler; candidate03 assembly
changes only slot4, other five files exact. Native03 fixture+UID/fingerprint/
publisher and actor-review-v2 eight views/two boards/motion parity. Normal test+
UID/prepare/install/fingerprint/publisher/register/recorder,normal-review-v1 with
eight pairs/two boards/correct four-facing comparison/assessment/evidence.
Normal catalog appends candidate03;root selection normal true/provisional eight
Continue verified;historical held flags preserved. tests/index companions/native900.
Pipeline,bible,current status,maintained/installed master-repair skill appended.

## Verification and scope
Stage444 checks/8 views/95 controlled20ms samples/2 wraps/6 restores+pause holds,
{stage['stableBoundedInputs']} stable inputs. Normal{proof['checks']} checks/8 full
saves/8 visible fresh Title Continues/16 captures/8 exact pairs,
{proof['stableBoundedInputs']} stable inputs. Both2931 owner non-log files unchanged,
zero failures/engine errors and exit0.475 named motion fields and8 roots equal
versus run02;only whole slot4 changed. All source/ruler/cycle/staged/normal pairs
and four-facing board inspected. No fullscene/continuous film/contact/full-family
acceptance. Normal catalog counts are coverage only. No live native process.

## Remaining work and next action
Carry and remaining held families need master/body/camera/grade matching. Then
full-set consistency/polish, continuous contact/flight/sole and equipment joins.
All four cardinal run improvements have independent normal eight-Continue proofs,
but full goal remains incomplete. Keep active task and scoped evidence.
'''
    (ROOT/'docs/MARSH_NORTH_RUN_NORMAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded North03 normal eight-Continue proof and passing repair lessons; skill mirrors equal; full goal incomplete.')
if __name__=='__main__':main()
