"""Record coherent staged South injury source and verified cosmetic idle join."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-injury-material-v1'

def contains(path,marker):
    with path.open(encoding='utf-8') as stream:return any(marker in line for line in stream)

def append_once(path,marker,text):
    if not contains(path,marker):
        with path.open('a',encoding='utf-8') as stream:stream.write(text)

def main():
    review=BASE/'actor-review-v1'
    assessment={'normalAdmission':False,'allFourteenPairedViewsInspected':True,'wholeSourceFamilyInspected':True,'pairedBoards':[f'paired-{i}.png' for i in range(4)],'material':'All complete body poses retain improved dry source ivory boot uppers and warm ivory/sage grade. Body opaque pixels exact in all12 composites.','effect':'Neutral warm white droplets at left glove, modest thin floor puddle. Common whole-effect scale; mature36x10px puddle fixedcenter54,173 through growth/recovery. Matte fluid distinct from body. Half-alpha recovery pose4 and absent pose5.','sourceConstraints':'Effects generated separately with built-in tool. No generated character/body pixels used; effects behind intact body. Existing injury/dry image subtraction rejected because differing anatomy would contaminate fluid layer.','joins':'Floor injury5 and recovery0 byte exact; recovery5 and first normal idle now exact selected idle0. Renderer cosmetic key reset verified in actual actor/grid.','pending':'Complete moving/family anatomy/grade review, other facings, normal source admission and full RunSave/Title Continue. Source body prone foreshortening remains provisional. Native APNG is captured pose illustration, not realtime recording/browser motion acceptance.'}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_south_injury_material.py'),run_name='__main__')
    lesson='''
## Marsh South white-fluid injury/recovery source and idle join — October 2, 2026

New character/marsh-south-injury-material-v1 candidate01 has six injury and six
recovery180ms poses,184square/p92,172/H148. Each opaque body pixel EXACT to
the complete South dry-collapse material source01. Separate built-in effect-only
generation exec-643ea690-8b23-4601-9864-cb306f10a98f retains prompt/request,
ordered old-fluid reference guide/raw/hash. Four droplets/puddle swatches at
ONE effect scale0.10495626822157435, calibrated mature width36; BOX/alpha128.
Dense swatches5x17,4x27,24x8,36x10. Whole effects behind unchanged bodies;
fixed floor puddlecenter54,173, recovery half-alpha at4/absent at5. No anatomy
mask/paint, reflection, per-pose scale or palette normalization. Reverse complete
body sequence follows existing recovery policy. Dry shutdown stays liquid-free.

404actual native actor/grid checks pass:14exact source pairs,12actor+player
restores and pause holds. Physical impact triggers six fall/six rise holds,
root fixed, nonfatal idle return. Injury5/recovery0 byte exact, recovery5/first
normal idle EXACT selected idle0.12opaque body invariants and12decoded source
APNG frames pass;12native APNG pose crops exact.76bounded inputs stable;2931owner
non-log files unchanged in scratchAPPDATA,exit0/engine0. All14paired views/four
boards and full source family inspected. Art remains UNSELECTED/provisional,
not full master-family polish, articulated contact or fullRunSave/TitleContinue.
Native APNG illustrates captured poses at180ms, not realtime film/browser review.

Earlier retained prejoin interval403checks/14captures/12restores passed controller
checks but observed first normal idle on old breathing pose1 instead of authored
idle0. scripts/grid_canvas.gd now clears Marsh player's old cosmetic key during
simulation-owned injury-ground/rise selection. Following normal idle starts fresh;
normal actor/controller and save schema unchanged. Final404check rerun proves
first draw equality and active-state restoration with this narrow renderer change.
Current normal catalog still uses old injury art until source admission; new
South exact art proof does not accept other-facing old material/endpoints.

Lesson: green injury traversal checks can miss cosmetic state after completion.
Compare actual first normal drawn source to authored last recovery, and preserve
pre-fix evidence. Separate source effect authoring preserves complete new anatomy;
do not derive fluid by subtracting differently drawn dry/injury bodies. Verify
body pixel invariance and fixed floor registration. Raw effect coloured fringe
had0high-chroma pixels at alpha128; binary whole-source packaging, no recolouring.
Shared documentation may be mapped by desktop readers: append milestone entries
without truncation and stream marker lookup rather than rewriting enormous files.

Review:character/marsh-south-injury-material-v1/actor-review-v1/index.html.
Next: normal provisional South dry/injury/rise source admission and full save/
visibleContinue checks when ready, other facing material corrections, then full
set consistency/polish. Full Marsh objective remains active and incomplete.
'''
    marker='## Marsh South white-fluid injury/recovery source and idle join — October 2, 2026'
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirror drift; do not overwrite'
    for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:append_once(p,marker,lesson)
    installed.write_bytes(maintained.read_bytes())
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: staged South injury/recovery

## Objective and acceptance
Full Marsh set matching master/style/camera/proportions/grade, then family polish.
Still active/incomplete. This milestone establishes coherent staged South fluid
sources and fixes observed normal cosmetic idle seam, not whole-family acceptance.

## Accepted decisions and constraints
Complete improved dry body, every opaque pixel exact. Injury fluid WHITE;
shutdown DRY. Separately generated effects behind bodies; no anatomy patching,
per-pose height fitting or palette mapping. Reversible work authorized, no exports.
All native probes scratchAPPDATA with before/after owner profile fingerprint.

## Current state
New character/marsh-south-injury-material-v1 sources/candidate01/actor-review-v1.
Built-in fluid-only raw/prompt/request/hash retained;12complete exact-body poses,
two six180ms states. Mature puddle36x10fixed54,173; recover4half-alpha/5none.
Normal catalog source selection unchanged. scripts/grid_canvas.gd narrowly resets
Marsh cosmetic key during injury/rise so normal idle resumes at authored idle0.
Prepare/build/review(+UIDcb1shinjm6v69)/fingerprint/publish/record tools added.
Pipeline/bible/current status and exact maintained/installed master-repair updated
by append; newest status milestone is near tail because mapped docs resist truncate.

## Verification
404native actual actor/grid checks,14exact source pairs,12actor+player restores,
all fall/rise holds and pause; nonfatal fixed-root return. Both floor handoff and
first normal idle exact.76bounded inputs stable;2931ownerfiles unchanged,exit0/
engine0.12exact opaque body matches,12source and12native decoded APNG frames.
All14views on4paired boards and full family sheet inspected. Prejoin403passing
checks retained; first-normal-idle seam observed there, fixed and revalidated.
No fullRunSave/TitleContinue or other-facing art acceptance; browser/realtime
motion unverified. South source head/torso/prone foreshortening still provisional.

## Next action
Admit improved South dry/injury/rise provisionally to normal ordered catalog and
verify full saves/fresh visible Title Continues through active/final phases.
Then correct other-facing collapse/injury/recovery grade/boot mismatches and
continue full coverage/whole-family consistency and polish.
'''
    (ROOT/'docs/MARSH_SOUTH_INJURY_MATERIAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded staged injury/recovery and actual first-idle correction; skill mirrors exact; full goal active.')
if __name__=='__main__':main()
