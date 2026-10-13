"""Record inspected complete alternating-run source and actual actor evidence."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1'
MARKER='## Marsh South complete alternating run and staged actor study — October 2, 2026'
LESSON='''
## Marsh South complete alternating run and staged actor study — October 2, 2026

South run candidate04 is a new complete alternating contact/passing/flight cycle,
still UNSELECTED/provisional. Five complete byte-preserved candidate03 poses in
new order3/4/2/0/5 plus independently authored full right-support passing06;
actual order is03[3,4,2,0],06passing,03[5]. No mirror, limb patch, recolour or
per-pose fit. Existing six100ms loop and selected run-south distance stride
0.11027027027027027cells explicitly preserved. Neutral147occupied calibration,
184canvas,p92/172,H148. Art size changes do not justify silently changing cadence.

Single selected walk3 complete pose nearest4x made the support side visually
explicit: correct viewer RIGHT planted foot/LEFT lifted foot. Passing05 source
exec-f135a5ba-5de8-4914-b347-105c357cac07 got correct side but almost level neutral
head; one scale.1821561338289963, passing68x148/ruler61x148 sampling from147target.
Retained whole source. Passing06 whole compression correction generation
exec-15dfa08c-5b7b-4499-b566-6b67a30aba15 uses selected body/pose, previous05
leg-side guide only, original master. Frozen exact prompts and ordered reference
SHAs/raws/originals retained.06 commonneutral scale.18170580964153277,
passing67x134/ruler62x147; lowering through authored knee/hip flexion rather than
shrinking anatomy. Raw05/06 and both packed comparisons visually inspected.
Candidate04 sixsizes63x144/64x141/63x130/63x146/67x134/63x132.

Actual normal Marsh.move/controller/main/grid/player in clear168world-unit
South furnished ColdStore route with whole-body envelope:438checks/8exactviews,
95controlled20ms simulation/render samples,2wraps,6actor-player restores/pause
holds, normal destination hysteresis returns selected walk.0fail/engine0/exit0.
87bounded source/controller inputs stable;2931owner non-log files unchanged
under scratchAPPDATA. Normal costs/failures remain, normal catalog unchanged.
All8paired views/two boards inspected: complete actor unobscured, warm ivory
uppers/sage/slate/charcoal retained, opposite contact and flight knees readable.
Passing head/body compression and moving pose joins remain provisional; right
passing134occupied versus left141, no per-pose normalization imposed.

Retained initial south-run-actor-04-2026-10-02 interval438checks/76fixture
speed-tolerance failures,8views/6restores/2wraps and stable87inputs/2931owner.
Per-frame trace measured1.37988281worldunits vs requested1.38 at room coordinates;
original is_equal_approx tolerance too strict for vector float precision.
Original fixture.gd and report/log/fingerprints retained. Correctedv2 checks
absolute difference<0.001WORLD UNITS; test label's 'submillimetre' is not a
physical unit claim. No speed/controller/gameplay change. Correct-v2 evidence
is south-run-actor-04-v2-2026-10-02. Do not repair art or controller from a failed
numeric fixture until actual per-frame state establishes the cause.

Player distance stride is a GLOBAL manifest field, not per-state timing. Later
load_manifest(append=true) otherwise preserves inherited stride implicitly;
package explicit selected stride and test unchanged before/after override.
Support side prose alone repeatedly failed. A complete correctly sided selected
pose reference succeeded without mirrored asymmetric identity or anatomy edits.
Still inspect generated support/bend/head/equipment and whole cycle; a correct
side does not certify compression, grade, contact, density or moving acceptance.

Review:character/marsh-south-run-material-v1/actor-review-v1/index.html.
NativeAPNG is six exact captured crops with100ms illustrative holds, not real
time film/contact evidence. No full RunSave/TitleContinue, natural routing/traffic,
helmet equipment joins or full family acceptance in this staged study.
Next: refine unequal passing compression and projected floor/contact joins at
shared anatomy scale, inspect moving run/idle/walk continuity; normal provisional
selection/fullcheckpoint Continue only after reviewed source is ready. Continue
other facings/run/carry and68remaining held family boards/full-set consistency.
Full master/style/camera/size/height/proportion/grade/polish objective active/incomplete.
'''
def main():
    assessment={'normalAdmission':False,'fullGoalComplete':False,'allEightViewsInspected':True,'pairedBoards':['paired-0.png','paired-1.png'],'sourceComparisonsInspected':['passing-05-unselected/comparison.png','passing-06-unselected/comparison.png','candidate-04/comparison.png'],'appearance':'Complete unobscured whole actor, warm ivory boot uppers/sage/slate with charcoal soles/gloves; adult head/torso joins materially closer to selected idle/walk.','phaseReview':'Both contact and flight legs alternate; new complete06 supplies correct right-support passing. Right passing compression differs visibly from left and remains provisional.','limits':'Controlled native95samples and eight held captures, not real-time film, articulated contact, full Save/Continue, natural traffic/equipment or entire family acceptance.'}
    (BASE/'actor-review-v1/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    (BASE/'candidate-04/review.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_south_run_actor.py'),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with p.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with p.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh South alternating run

## Objective and acceptance
Full master-matched Marsh set/consistency/polish active/incomplete. Complete South
run candidate04 now alternates both legs; unselected and provisional motion/contacts.

## Accepted decisions and constraints
Correctly sided whole selected walk3 reference, original asymmetric front master,
147occupied neutral calibration/H148metadata, no per-pose fitting/mirror/patch/
recolour. Existing six100ms loop and0.11027027027027027cell stride retained.

## Current state
character/marsh-south-run-material-v1 now has frozen passing05/06 requests/raws,
whole packed comparisons/rulers, assembled candidate04 (03[3,4,2,0],06pass,03[5]),
actor-review-v1 exact source/native boards/verification/illustrativeAPNG. New
guide/packager/assembler/native fixture+UIDcm3shrunm8v80/fingerprint/publisher/recorder
tools. Pipeline/bible/status/skill mirror appended. Catalog/runtime unchanged.

## Verification
438checks/8exact captures/95controlled20ms samples/2wraps/6actor-player restores
and pauseholds;0fail/engine0/exit0.87bounded inputs stable,2931ownerfiles unchanged
scratchAPPDATA. Raw05/06, both packed comparisons, fullcycle sheet and all8native
views/two boards inspected. Original failed speed-tolerance interval/fixture kept:
1.37988281actual vs1.38expected, fixed absolute0.001worldunit tolerance only.
No fullRunSave/TitleContinue, realtimefilm, articulated contact/equipment acceptance.

## Next action
Refine right134-vs-left141passing compression and projected floor/contact joins
through whole source authoring/registration, then run/idle/walk moving continuity.
Normal provisional selection/fullcheckpoint Continue when reviewed source ready.
Other run facings/carry,68remaining held inventoryboards and full consistency/polish
remain. No live native process; correctedv2 audit is terminal exit0.
'''
    (ROOT/'docs/MARSH_SOUTH_RUN_ACTOR_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded staged complete alternating run, honest limits and exact skill mirror.')
if __name__=='__main__':main()
