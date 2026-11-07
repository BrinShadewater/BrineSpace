"""Record inspected West corrected dry and exact-body coolant studies."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1]
MARKER='## Marsh West dry and white-fluid actual actor studies — October 2, 2026'
LESSON='''
## Marsh West dry and white-fluid actual actor studies — October 2, 2026

West dry candidate02 remains unselected/provisional: exact selected31x147idle,
whole corrected first44x134pose and four complete retained source01 poses.
Source01 neutral scale .34106728538283065 and correction .19367588932806323 each
calibrate to selected147occupied rows; sampled neutral32x147, declaredH148.
First loses13rows versus source01two; requested7notforced by per-pose fitting.
Later59x113/78x87/97x57/157x40, own left-facing master/bare visible temple retained.
No reflected East body or invented near-side temple hardware. Native held review
shows complete unobscured figures, fitted adult head/detail density and warm
ivory/sage/boot uppers with charcoal sole material. Prone length/camera/contacts
and moving first-dip/head/torso joins remain provisional family work.
Actual normal die/main/grid/player249checks/8exact sources/6actor-player restores,
66controlled20ms samples;0fail/engine0/exit0.70bounded inputs stable;2931owner
non-log files unchanged scratchAPPDATA. Both boards/all8views inspected;
pause/fixedroot/zero locomotion offsets and final20secsettled hold pass.

West white-fluid injury/rise candidate01 retains all12complete corrected dry
body pixels exact.4reused authored independent148-density swatches behind body,
whole glove droplet anchors(70,124)/(72,142), fixed puddlecenter(72,172), growth
then penultimate recovery half-alpha/finalnone. Puddle stays on floor as body
extends left; do not attach it to each later hand position. Fall5/rise0 and
rise5/selectedidle0 byte-exact;12opaque body comparisons pass. Actual physical
impact/fall/rise/grid404checks/14exact sources/12actor-player restores,0fail/engine0/
exit0.115bounded inputs stable;2931owner files unchanged scratchAPPDATA. Existing
renderer idle seed reset supplies exact fresh idle0; no new runtime/schema or
normal catalog change in either study. All4paired boards/14views inspected;
white droplets and stationary puddle visible, complete figures unobscured.
Both source12 and native12 APNG decoded frames exact, oneplay180ms holds.

Retained occluded-glove-draft before native interval: first/second placements
(78,124)/(82,142) left only3/30visible pixels, first narrative nearly vanished
behind bent leg. Whole insert translations to(70,124)/(72,142) give39/55visible
pixels without body changes. A few nonzero pixels are not sufficient visual
effect acceptance. Inspect narrative visibility and layering at runtime scale;
do not patch the leg or paint coolant onto anatomy. Floor-puddle occlusion during
rise is coherent exact-body layering, distinct from invisible initiating droplets.

Native APNGs illustrate captured poses, not realtime films. No full RunSave/
TitleContinue, natural traffic, articulated limb contact, browser moving review
or entire family art acceptance. All four repaired damage facings retain
provisional motion/proportion/grade refinements; selected states aren't proof.
Reviews:character/marsh-west-collapse-material-v1/actor-review-v1/index.html and
character/marsh-west-injury-material-v1/actor-review-v1/index.html.
Next: normal provisional West damage selection/fullcheckpoint Continue, then
full-set coverage/master/camera/size/height/proportion/grade and moving polish.
Full Marsh objective stays active and incomplete.
'''
def main():
    dry=ROOT/'character/marsh-west-collapse-material-v1';injury=ROOT/'character/marsh-west-injury-material-v1'
    assessment={'normalAdmission':False,'allEightPairedViewsInspected':True,'pairedBoards':['paired-0.png','paired-1.png'],'material':'Own left-facing fitted adult body/bare near temple, warm ivory/sage and boot uppers with charcoal sole surfaces retained.','visibility':'All8whole figures unobscured in furnished clear site.','proportions':'First44x134 versus selected31x147; complete articulation rather than per-pose fitting. Later/prone and moving joins provisional.','scope':'249checks/8exact sources/6restores; no full Save/TitleContinue or real-time motion acceptance.'}
    (dry/'actor-review-v1/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    assessment={'normalAdmission':False,'allFourteenPairedViewsInspected':True,'pairedBoards':[f'paired-{i}.png' for i in range(4)],'sourceComparisonInspected':True,'material':'Exact complete warm ivory/sage bodies and own left-facing identity; white fluid visible beside glove/on stationary floor.','effectRegistration':'Whole droplets39/55visiblepixels; floor puddle fixed72/172 through body motion, growth/recovery fade; layering inspected.','retainedDraft':'occluded-glove-draft3/30visiblepixels retained before native interval; complete insert translation correction, no anatomical edits.','limits':'Held/controller evidence only; no full Save/TitleContinue, realtime/browser motion, natural traffic or articulated limb contact acceptance.'}
    (injury/'actor-review-v1/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    for name in ['publish_marsh_west_collapse_actor.py','publish_marsh_west_injury_material.py']:runpy.run_path(str(ROOT/'tools'/name),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh West damage studies

## Objective and acceptance
Full master-matched Marsh set/consistency/polish active/incomplete. West staged
dry candidate02 and exact-body white-fluid injury/rise candidate01 provisional.

## Accepted decisions and constraints
Own West left-facing master, bare near temple; no reflected East source.
One147occupied neutral scale per raw source/H148metadata, whole figures only.
Exact bodies/independent coolant behind, fixed floor puddle. Normal flags/save
rules and owner profile/layouts preserved. No patch/fit/recolor/mirror.

## Current state
West collapse8review views and injury14review views all inspected. New actual
actor fixtures/pairedUIDcj9whclpm5v77 andck1whinjm6v78, prepare/build/fingerprint/
publish/record helpers; retained3/30visiblepixel coolant draft and corrected
39/55whole swatch placements. Pipeline/bible/status and identical skills updated.
No runtime/schema/catalog admission changes in these studies.

## Verification
Dry249checks/8exact sources/6restores/70boundedinputs. Injury404checks/14exact
sources/12restores/115boundedinputs. Each0fail/engine0/exit0,2931ownerfiles unchanged
scratchAPPDATA. All6boards/22views inspected; pause/root/settledhold/freshidle
joins exact.12opaquebody comparisons/source/native APNG frames exact. Captured
poses not realtime films; no full Save/TitleContinue or full-family acceptance.

## Next action
Provisional normal West damage selection then20full saves/fresh visible Continue
proof. Full-set master/camera/size/height/proportion/grade audit and motion polish
remain, including head/torso/prone and articulated contacts across facings.
'''
    (ROOT/'docs/MARSH_WEST_DAMAGE_STUDY_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded West dry/injury native studies; full Marsh goal active.')
if __name__=='__main__':main()
