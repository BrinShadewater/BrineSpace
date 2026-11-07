"""Record reviewed mild passing and exact whole contact registration evidence."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
MARKER='## Marsh South mild passing and shared sole-plane run revision — October 2, 2026'
LESSON='''
## Marsh South mild passing and shared sole-plane run revision — October 2, 2026

South run candidate05 remains unselected/provisional, now has a milder complete
right passing pose and whole contact registrations. Selected idle actual occupied
58x147, bottom-exclusive171, canvas184,pivot92/172,H148. Shared RUN planted-sole
bottom-exclusive172 explicitly aligns to runtime pivot, not exact selected-idle
occupied bounds; don't infer changing the idle or normalising all pose heights.
Whole translations: leftcontact-1Y, leftpassing+1Y, rightcontact-1Y, others0.
Whole cropped RGBA bodies unchanged by translation, no clipping or limb patch.
Flight poses retain16/14dense-pixel clearance. Existing six100ms looping and
0.11027027027027027cell distance stride unchanged. No controller/catalog change.

Passing07 requested right support but generated LEFT despite the correctly sided
single walk3 reference when multi-pose comparison was also supplied. Full source
exec-a9d2c8e4-0968-4bbd-8e91-3a20f97fbdde retained with exact frozen prompt/refSHAs;
one neutral scale.1701388888888889, passing67x141/ruler60x147. Rejected as right
phase; do not mirror or patch it. Source08 instead used single selected walk3
FIRST, single selectedidle0 SECOND, original front master THIRD; multi-pose guide
omitted. Both whole selected references nearest4x without artwork change.
Source08 generation exec-81e7121a-c065-4102-9eb1-33040ca2ff34 retains exact
request/raw/original, right support preserved and smaller natural knee/hip dip.
One neutral BOX scale.175, passing63x141/ruler57x147. Original master asymmetric
right temple/viewerLEFT remains; no reflected limbs or per-pose height fitting.
Matching141row passing silhouettes are output observations, not anatomy proof.
Neutral sampled57width differs from selected58; no geometry equality claimed.

Candidate05 sizes63x144/64x141/63x130/63x146/63x141/63x132. Complete source08
replaces phase4 only; complete04 retained poses plus ground registration above.
Warm fitted adult head/torso, ivory uppers/sage/slate/charcoal materials are held
review improvements; complete identity/head/equipment/moving contacts provisional.
Raw07/08, both packed comparisons, full before/after sheet and all8native views
on two paired boards inspected. Actor unobscured in clear furnished ColdStore.

Fresh actual normal Marsh.move/controller/main/grid/player staged candidate05:
444checks/8exact sources/95controlled20ms samples/2wraps/6actor-player restores
and pause holds, normal destination slowing to selectedwalk;0fail/engine0/exit0.
Actual loaded textures check planted-bottom172 or airborne clearance.115bounded
source/controller inputs stable,2931owner non-log files unchanged scratchAPPDATA.
Normal costs/failures retained; diagnostic fixture is tools/review_marsh_south_run05_actor.gd
with pairedUIDcn4shrnm9v81. Native audit south-run-actor-05-2026-10-02 terminal.

Independent preceding04-v2 comparison:475named motion-field checks across95samples
(elapsed,slot,running,foot,playerPhase) EXACT, all8capture roots EXACT. Submitted
source changes exclusively contact0/1/3 whole translation and new4whole passing;
idle/flight2/flight5/selectedwalk sources exact. No whole-framebuffer equality or
real-time/contact acceptance inferred. compare_marsh_south_run05.py reproduces it.
Native captured-poseAPNG sixframes100ms is illustrative, not a realtime film.
Earlier04-v2 scoped438passed evidence retained separately from original04failed
float-tolerance fixture; no edits to historical sources/reports. Revised05 fixture
names tolerance correctly0.001WORLD UNIT, no physical millimetre interpretation.

Lesson: a multi-pose motion comparison can reintroduce opposite leg conditioning
even beside a correct single stance. Put the exact desired whole stance FIRST
and single anatomy master next; still inspect actual generated supporting foot.
Review head/pelvis compression at common neutral scale, and register complete
planted figures to declared foot plane while preserving airborne clearance.
Never stretch a pose to match occupied bounds or relocate only the boot.
Separate unchanged controller trace from changed art; refreshed native interval
is required for a new source, old passed interval proves only its old source.

Review:character/marsh-south-run-material-v1/actor-review-v2/index.html.
Next: normal provisional candidate05 admission/full RunSave and actual fresh
TitleContinue source/root/cadence/phase/pause checks, then remaining run facings,
carry and68held-family boards with cross-family motion/contact/material polish.
No fullSave/TitleContinue, natural traffic, helmet joins or whole family acceptance
yet. Full master/style/camera/size/height/proportion/grade/polish goal active/incomplete.
'''
def main():
    assessment={'normalAdmission':False,'fullGoalComplete':False,'allEightViewsInspected':True,'pairedBoards':['paired-0.png','paired-1.png'],'sourceComparisonsInspected':['passing-07-unselected/comparison.png','passing-08-unselected/comparison.png','candidate-05/comparison.png'],'appearance':'Complete actor unobscured; warm matte ivory uppers/sage/slate/charcoal retained. Right passing dip reduced without shrink/patch; head/torso joining selected idle/walk closer.','registration':'Whole contact0/1/3 translates -1/+1/-1dense rows; planted bottoms172 align runtimepivot. Selected idle bottom171 remains unchanged. Flight clearances16/14dense retained.','phaseReview':'Complete alternating contact/passing/flight both sides; equal141passing heights observed, not exact anatomy or continuous contact proof.','limits':'Controlled native95samples/8heldviews, not realtime film, fullSave/TitleContinue, natural traffic/equipment or full family acceptance.'}
    (BASE/'actor-review-v2/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n');(BASE/'candidate-05/review.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_south_run05_actor.py'),run_name='__main__')
    runpy.run_path(str(ROOT/'tools/compare_marsh_south_run05.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh South run revision05

## Objective and acceptance
Full master-matched Marsh set/consistency/polish active/incomplete. Candidate05
unselected/provisional, milder complete right passing and shared run sole plane.

## Accepted decisions and constraints
Whole selected walk3 first/single idle0 anatomy next/original asymmetric master.
147occupied neutral calibration/H148metadata, no mirror/patch/recolour/per-posefit.
Six100ms loop and selected0.11027027027027027cell stride retained. Contact-plane172
matches runtimepivot; selected idle actualbottom171 intentionally unchanged.

## Current state
character/marsh-south-run-material-v1 retains wrong-side07source and correct08
source/request/raw/ruler/packedcomparison; candidate05 complete sixposes and
actor-review-v2. Rightpass08 replaces04phase4; whole contact0/1/3Y=-1/+1/-1,
others unchanged. No catalog/controller changes. Guide/packager/native fixture+
UIDcn4shrnm9v81/fingerprint/publisher/tracecompare/record tools added. Pipeline,
bible,status and installed skill exact mirror appended; historical04 evidence kept.

## Verification
444checks/8exactviews/95controlled20ms samples/2wraps/6actor-player restores and
pause holds;0fail/engine0/exit0.115bounded inputs stable;2931ownerfiles unchanged
scratchAPPDATA.475named previous04-v2 motion comparisons and8captureroots exact,
only expected4source changes. Whole translated-body RGBA exact/no clip, common
loaded contactplane172/flight16/14clearance. Allcomparisons and8nativeviews inspected.
No fullSave/TitleContinue, realtimefilm, articulated contact/equipment acceptance.

## Next action
Normal provisional candidate05 admission/fullRunSave and fresh actualTitleContinue
source/root/cadence/phase/pause checks. Then other run facings/carry,68remaining
heldfamilyboards and full-library motion/contact/proportion/grade polish.
No live native or recorder process after this milestone;05native terminalexit0.
'''
    (ROOT/'docs/MARSH_SOUTH_RUN_05_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8');print('Recorded05 source/registration, fresh native and exact motion comparison; full goal incomplete.')
if __name__=='__main__':main()
