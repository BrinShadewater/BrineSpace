"""Record closer whole first-half consistency and exact staged evidence."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-east-run-material-v1'
MARKER='## Marsh East whole first-half09 and coherent run03 study — October 2, 2026'
LESSON='''
## Marsh East whole first-half09 and coherent run03 study — October 2, 2026

New COMPLETE first-half09 source exec-2fa06824-9681-4848-b165-cfc9ee3970af
retained with exact frozen prompt, three ordered reference hashes and original
generated path/rawSHA. Selected single East idle PRIMARY anatomy/material/camera,
unchanged whole first3candidate02 figures nearest4x ONLY leg arrangement guide,
own original East master identity/authentic temple and ankle hardware authority.
Four authored figures near-contact/near-support passing/far-knee flight/neutral.
One neutral BOXscale .24915254237288137,147occupied calibration target; sampled
sizes103x145/68x146/96x136/ruler37x146. One-row ruler sampling difference recorded,
not secretly fitted.184canvas,p92/172,H148; contact/passing/ruler whole-registered
bottom172, flight source-relative. Complete alpha128 cells/no-clipping pixel
counts checked. No mirror, patches, palette repair or per-pose fitting.

Candidate03 uses exactly those first3whole frames plus unchanged candidate02
second half: half02farcontact,pass08far-support,half02near-knee flight. Six source
file copies byte-identical, sourceAPNG sixdecodedframes exact, six100msloop and
explicit existingEast stride0.11027027027027027cells retained. Sizes103x145/
68x146/96x136/101x146/68x144/90x140. Complete raw, old/new first-half board, full
six-pose board and common-pivot selectedidle/newruler/selectedwalk/contact board
visually inspected. First-half head/torso now closer to second-half rather than
previous135/137/127compressed occupied heights. This is whole-source reauthoring,
not an occupied-height normalization. Near/far thigh-knee-boot order retained;
warm ivory/sage/slate/charcoal/material and original small ankle hardware reviewed.
Neutral37x146vsselected32x147 retains toe/suit profile difference; no exact anatomy
or equal-width claim. Body/head/profile continuity improved, provisionally ready
for normal-catalog/fullSave/Continue verification. Final motion, full-family
camera/grade/proportion acceptance and polish still pending.

Fresh staged ACTUAL normal Marsh.move/main/grid/player/native East03:
444checks/8exactsource-crop pairs/95controlled20ms samples/2wraps/6actor-player
restores+pauseholds,normal slowingwalk;0fail/engine0/exit0.118bounded inputs stable
during native interval,2931owner nonlogfiles unchanged scratchAPPDATA. Fixture
UIDcs9ehrun03v86 paired. Existing validated horizontal furnished-site route;
no gameplay/nav/controller changes. Dedicated room placement authors test site
for free; normal global freebuild/failureflagsfalse not paidroomcost proof.
All8source/native CROPS inspected in two boards; readability beside furniture,
head/body joins reviewed. No full-scene occlusion or continuous film claim.
475NAMEDmotion comparisons (elapsed,slot,running,foot,playerPhase) across95samples
exactly equal preceding02, eight capture roots equal; only source slots0/1/2
change, secondhalf/idle/walk exact. No full-framebuffer/contact equality inferred.
NativeAPNG six exact captured crops100ms illustrativeholds only.

Lesson: matching first-half whole anatomy with selected idle while treating prior
compressed poses as leg-order references can improve a cycle without changing
cadence or controllers. Inspect neutral plus full stance joins; scale-calibration
and occupied height remain diagnostic, not anatomy acceptance. Preserve source
phase order and compare named motion fields to distinguish art revisions from
movement changes. Original ankle buckles remain authentic (preceding correction).

Review:character/marsh-east-run-material-v1/actor-review-v3/index.html.
Normal catalog unchanged, candidate03 still unselected during this staged study.
NEXT admit03 provisionally via normal catalog and verify all8fullRunSave/fresh
visibleTitleContinue states plus continued motion; inspect whole four-facing run
family again. Then West/North run/carry/remaining held families and full-set
consistency/polish. Full Marsh master/style/camera/size/height/proportion/grade
and full-set goal ACTIVE/INCOMPLETE. No live native process after this milestone.
'''
def main():
    review=BASE/'actor-review-v3'
    assessment={'normalAdmission':False,'fullGoalComplete':False,'allEightViewsInspected':True,'inspectedViewScope':'Exact sources/native framebuffer crops in two paired boards; no fullscene or continuous-film claim','sourceComparisonsInspected':['half-09-unselected/comparison.png','candidate-03/comparison.png','actor-review-v3/source-ruler-comparison.png'],'appearance':'First-half head/torso closer to second half. Quiet warm matte original suit retained. Ruler37x146vsselected32x147 partly toe/suit profile; exact geometry unaccepted.','phaseReview':'Distinct near/far contacts/support passing/knee-forward flights retain whole leg continuity. Continuous articulated contact remains unverified.','readiness':'Provisionally ready for normal-catalog and fullSave/visibleContinue validation. Final full-family camera/grade/proportion/motion polish pending.','limits':'Staged actual normal movement only. No fullSave/TitleContinue/whole scene occlusion/realtime film/full-set acceptance.'}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n');(BASE/'candidate-03/review.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_east_run03_actor.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh East run03

## Objective and acceptance
Full master-matched set/consistency/polish active/incomplete. East03 body/head
joins improved and provisional source is ready for normal-catalog/fullSave/
visibleContinue validation. Normal catalog still unchanged at this milestone.

## Accepted decisions and constraints
Selected idle anatomy/material/camera PRIMARY; prior complete first3poses only
leg-order guide; original own East master identity/hardware. Authentic ankle
buckles retained. Whole-source reauthoring, one neutral scale, no perposefit/
patch/mirror/recolour.184canvas,p92/172,H148,six100msloop,East stride unchanged.

## Current state and changed files
character/marsh-east-run-material-v1: exact09request/raw/originalID/hashes,
whole nearest4x leg guide/provenance, four complete half09figures/recipe/old-new
board, candidate03six byte-identical files/manifest/recipe/APNG/comparison/review,
actor-review-v3 source/ruler/action and two exactsource/nativecrop boards/scoped
verification. New prepare-half09/build-half09/build03/fixture+UID/fingerprint/
publisher/comparison/recorder tools. Pipeline/bible/status/master-repair mirrors
appended. No gameplay/controller/nav or normal catalog modifications.

## Verification and scope
444checks/8source-crop pairs/95controlled20ms samples/2wraps/6restores+pauseholds/
normal walk slowing;0fail/engine0/exit0.118bounded inputs stable during interval,
2931owner nonlogfiles unchanged scratchAPPDATA.475namedcontrollerfields+8roots
exactvs02; only sources0/1/2change. All8source/nativecrops/whole comparison boards
inspected. Ruler147target samples146;37widthvsselected32 noexactgeometryclaim.
No fullSave/TitleContinue,continuousfilm/contact,fullscene/fullfamily acceptance.
Native session10058 terminal0. Site freefixtureplacement not paid-cost proof.

## Remaining work and next action
Normal provisional East03catalog admission + independent full8checkpoint/fresh
visibleTitleContinues/resumedrunning validation; four-facing family source review.
Then West/North run/carry, heldfamilies, full consistency/polish. Keep goal active.
'''
    (ROOT/'docs/MARSH_EAST_RUN_03_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded improved East03wholefirsthalf, staged444+475motion proof; skills mirrored; full goal incomplete.')
if __name__=='__main__':main()
