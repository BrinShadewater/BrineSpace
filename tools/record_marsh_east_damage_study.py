"""Record inspected East staged collapse and exact-body coolant family."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1]
MARKER='## Marsh East dry and white-fluid actual actor studies — October 2, 2026'
LESSON='''
## Marsh East dry and white-fluid actual actor studies — October 2, 2026

East dry candidate01 remains unselected/provisional: exact selected32x147 idle,
five complete generated lowered figures, one .3202614379084967 neutral scale,
sampled neutral30x147, declaredH148 unchanged. Source collapse occupied widths
37/52/83/109/171 and heights140/115/91/53/41; first dip7rows versus old11. Whole
actor rendering inspected; restrained adult head/detail density, warm ivory/sage
and ivory boot uppers retained. Charcoal soles/heels distinct from boot uppers.
Prone length/camera and moving head/torso/contact joins remain provisional.
Actual normal die/main/grid/player staged study249checks/8exact sources/6actor-
player restores/66controlled20ms samples,0fail/engine0/exit0.52bounded inputs stable;
2931owner non-log files unchanged under scratchAPPDATA. Both boards/all8views
inspected, whole bodies unobscured, pause/fixed root/final20sec hold verified.

East white-fluid injury/rise candidate01 keeps all12complete dry body pixels
exact; reuses4authored independent148-density swatches behind the body. Visible
glove droplets whole-translated to(106,124)/(106,134); floor puddle center(122,172)
fixed through growth/recovery, then half-alpha/none. Body extends to the right,
so a stationary puddle does not follow every later hand position. Do not repaint
anatomy or move floor-fluid with hand merely to match old guide subtraction.
Fall5/rise0 and rise5/selectedidle0 byte-exact,12body comparisons pass.
Actual physical impact/fall/rise/main/grid/player404checks/14exact sources/12actor-
player restores,0fail/engine0/exit0.97bounded inputs stable;2931owner files unchanged.
All4paired boards/14views inspected. First normal idle exact, pause/fixedroot pass;
source12 and native12 APNG decoded frames exact. Existing renderer idle seed
reset reused; no new runtime/schema changes or catalog admission in either study.

Retained occluded-first-drop-draft: first swatch(98,114) behind exact body yielded
ZERO visible effect pixels. This is a source placement failure, not a native
test interval. Complete swatch translation to(106,124) yields38visible pixels,
body remains exact. Lesson: composing behind an intact body preserves anatomy
but can completely hide an effect. Check visible pixels and rendered silhouette;
do not promote a successful opaque-body invariant into fluid narrative acceptance.
Later puddle partially occluded by forearm in pose4 (156visiblepixels versus237
full); this is coherent layering, not license to cut an anatomical hole.

Held native/source APNGs are illustrative one-play180ms poses, not realtime film.
No full RunSave/TitleContinue, natural traffic, articulated limb world contact,
browser moving acceptance or full-family art completion. Both families provisional.
Reviews:character/marsh-east-collapse-material-v1/actor-review-v1/index.html and
character/marsh-east-injury-material-v1/actor-review-v1/index.html.
Next: provisional normal East selection/fullcheckpoint Continue family proof,
West whole-source repair and entire Marsh master/style/proportion/grade motion
consistency/polish. Full objective stays active and incomplete.
'''
def main():
    dry=ROOT/'character/marsh-east-collapse-material-v1';injury=ROOT/'character/marsh-east-injury-material-v1'
    dry_assessment={'normalAdmission':False,'allEightPairedViewsInspected':True,'pairedBoards':['paired-0.png','paired-1.png'],'material':'Warm ivory/sage, fitted adult side profile, ivory boot uppers and charcoal soles retained in renderer.','visibility':'All8whole source/native figures unobscured at clear furnished site.','proportions':'Selected32x147, sampled ruler30x147; firstdip37x140. Head/equipment density improved relative to old guide, moving/prone/contact provisional.','scope':'249checks/8exact sources/6actor-player restores; no full checkpoint/Continue or realtime motion acceptance.'}
    (dry/'actor-review-v1/visual-assessment.json').write_text(json.dumps(dry_assessment,indent=2)+'\n')
    injury_assessment={'normalAdmission':False,'allFourteenPairedViewsInspected':True,'pairedBoards':[f'paired-{i}.png' for i in range(4)],'sourceComparisonInspected':True,'material':'Exact complete warm ivory/sage bodies, matte gloves/soles; white droplets and stationary floor puddle visible.','effectRegistration':'Glove-side droplets and stationary puddle growth/fade inspected; partial forearm occlusion intentional.','retainedDraft':'occluded-first-drop-draft first swatch0visiblepixels; corrected whole translation yields38, no body edits.','scope':'404checks/14exact sources/12restores; exact injury/recovery/freshidle joins. No full Save/TitleContinue, real-time motion, articulated contact or whole-family acceptance.'}
    (injury/'actor-review-v1/visual-assessment.json').write_text(json.dumps(injury_assessment,indent=2)+'\n')
    for helper in ['publish_marsh_east_collapse_actor.py','publish_marsh_east_injury_material.py']:runpy.run_path(str(ROOT/'tools'/helper),run_name='__main__')
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill drift'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
        with path.open(encoding='utf-8') as stream:present=any(MARKER in line for line in stream)
        if not present:
            with path.open('a',encoding='utf-8') as stream:stream.write(LESSON)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh East damage study

## Objective and acceptance
Full master-matched Marsh set and consistency/polish active/incomplete.
East dry/injury/rise candidate01 provisional, unselected normal catalog.

## Accepted decisions and constraints
Complete authored dry poses, selected147occupied neutral calibration/H148metadata.
Independent coolant effects behind exact bodies, fixed puddle. No body patch,
pose fit/recolor/mirror. Normal flags/save rules and owner profiles unchanged.

## Current state
East collapse raw/prompt/ref hashes, candidate01 and8review views retained.
East injury frozen reuse provenance,12exact-body poses and14review views retained.
Both native fixtures/pairedUIDs, fingerprint/publish/prepare/build/record helpers.
Occluded first-drop source draft preserved; whole translation corrected before
native interval. Pipeline/bible/status and identical skill mirrors updated.

## Verification
Dry249checks/8exact sources/6restores/52boundedinputs. Injury404checks/14exact
sources/12restores/97boundedinputs. Both0fail/engine0/exit0; each2931ownerfiles
unchanged scratchAPPDATA. All6boards/22views inspected. Pause/fixedroot/settled
hold and injury/freshidle joins exact. APNG decoding exact; not real-time films.
No full checkpoint/Continue or whole-family art/moving/contact acceptance yet.

## Next action
Provisional normal East selection with20full checkpoint/fresh visible Continue
proof, then West damage identity/density/material repair and full-set moving polish.
Keep East head/torso/camera/prone comparisons provisional until motion accepted.
'''
    (ROOT/'docs/MARSH_EAST_DAMAGE_STUDY_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded provisional East dry/injury studies; full goal active.')
if __name__=='__main__':main()
