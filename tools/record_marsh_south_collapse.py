"""Record the source-only milestone without changing runtime or owner selections."""
from pathlib import Path
import json,runpy
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-south-collapse-material-v1'

def main():
    review=BASE/'native-review-v1'
    assessment={'normalAdmission':False,'status':'retained improved dry material candidate; actual actor/temporal acceptance pending','reviewedNativeSlots':list(range(6)),'reviewedSourceSheet':'../candidate-01/comparison.png','observations':['Whole ivory boot uppers and warmer ivory/sage grade are closer to selected South idle than old dark/cool collapse.','Initial candidate pose is byte-exact selected idle; old selected death initial pose still has dark boots.','New neutral occupied61x148 versus selected idle58x147: declared148 ruler is distinct from occupied bounds.','Whole pose occupied widths65,63,69,89,146 and heights127,105,83,50,36 at one global scale. Old corresponding poses70x126,66x105,67x85,93x60,170x40.','Final new silhouette is24pixels narrower (14.1%) than old; stronger foreshortening/body compression may explain it, but old motion guide is not body-length authority. Do not force old bounds with per-pose scaling.','Lowering-to-prone head/torso/limb joins need moving native actor inspection. Current captures share prescribed source ground-plane registration, not proven live hand/knee contact.','Pose2 still resembles a deep squat; prompt label knees contact does not certify anatomical floor contact.'],'pending':['Actual actor dry shutdown playback with normal grid draw placement, finite hold and master/camera/material review.','Coherent white-fluid injury and rise source family after dry basis accepted.','Remaining full-set coverage and four-direction material/proportion polish.'],'browserMotionReviewed':False}
    (review/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
    runpy.run_path(str(ROOT/'tools/publish_marsh_south_collapse.py'),run_name='__main__')
    lesson='''
## Marsh South dry-collapse material source study — October 2, 2026

New character/marsh-south-collapse-material-v1 retains five complete generated
collapse poses and a neutral ruler, exact frozen prompt/ordered references/raw
execution hash, plus byte-exact selected South idle as initial animation pose.
Built-in generation exec-e8ab4dbe-5622-43be-89de-0b8d74dfcc1c. Candidate01 is
UNSELECTED: six180ms holds,184square/p92,172/H148. Binaryalpha128, ONE neutral
BOXscale0.3070539419087137 and complete whole translations; no limb patches,
mirroring, per-pose height fitting or palette normalization. Warm ivory boot
uppers/material now closer to selected idle. Head/torso/floor joins still provisional.

217 native source-player checks pass, six native/source pairs exact, all six
decoded APNG holds exact180ms with one play. Finite player holds final source
past20seconds.32 bounded inputs stable;2931 owner non-log files unchanged through
scratchAPPDATA interval, exit0/engine0. All six native boards and source sheet
inspected. These fixed-anchor captures do NOT prove actual actor contact,
injury/recovery, normal catalog admission or full RunSave/Continue. Fingerprint
does not freeze every unrelated catalog artwork. Browser motion not reviewed.

New occupied widths65,63,69,89,146; heights127,105,83,50,36. Old motion guide
widths70,66,67,93,170; heights126,105,85,60,40. Neutral61x148 versus selected
idle58x147. Do not equate declared ruler with occupied height. Prone new24pixels
shorter/14.1% than old; old pose-only source is not body-length authority, and
foreshortening is not grounds to stretch a floor pose. Judge master anatomical
density and camera/body orientation instead. Prompt labels such as knees contact
do not establish real contact: pose2 appears deep squat, pose3 knees/hands down.
Finite review media must play once (APNGloop1), not loop0 indefinitely.

Next: actual staged actor shutdown placement/temporal review, then coherent
white-fluid injury/rise sources. Existing injury/rise and normal catalog unchanged.
Full Marsh goal remains active/incomplete. Review:
character/marsh-south-collapse-material-v1/native-review-v1/index.html.
'''
    maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
    installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
    assert maintained.read_bytes()==installed.read_bytes(),'skill mirrors drift; do not overwrite'
    marker='## Marsh South dry-collapse material source study — October 2, 2026'
    for path in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',maintained]:
        text=path.read_text(encoding='utf-8')
        if marker not in text:path.write_text(text+lesson,encoding='utf-8')
    installed.write_bytes(maintained.read_bytes())
    status=ROOT/'docs/CURRENT_STATUS.md';text=status.read_text(encoding='utf-8')
    if marker not in text:status.write_text(lesson.lstrip()+'\n'+text,encoding='utf-8')
    handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh South dry material source

## Objective and acceptance
Full master-matched Marsh set and family polish. Still incomplete. This milestone
establishes an improved staged dry-collapse material source, not normal acceptance.

## Accepted decisions and constraints
Selected South idle/master control identity, matte ivory/sage material and density.
Old collapse supplies motion only. Whole poses, one neutral scale, no isolated
anatomy painting or per-pose height fitting. Normal shutdown dry; injury liquid white.
All native probes use scratchAPPDATA and fingerprint owner profile before/after.

## Current state
New character/marsh-south-collapse-material-v1 sources/candidate01/native-review-v1.
Exact prompt/request/raw provenance retained; generator execution ID in request.
New tools prepare/build/fingerprint/review/publish/record_marsh_south_collapse,
review .gd UID paired. Runtime/catalog untouched. Pipeline, bible, status and
maintained/installed master-repair skill updated with scoped evidence/lessons.

## Verification
217 native source-player checks;6 exact source pairs;6 exact decoded APNG180ms
holds, one play.32 bounded inputs stable;2931 owner non-log files unchanged.
Exit0/engine0; six native boards/source sheet inspected. LFS rules coverPNG/APNG.
No actual actor contact, full Save/Continue or browser moving-view acceptance.
Candidate neutral61x148vsidle58x147; prone146x36vsold170x40. Better boots/grade,
but compressed floor build and head/torso moving joins remain provisional.

## Next action
Stage actual dry shutdown with normal grid/actor and this explicit manifest; review
placement and moving collapse against master without stretching prone bounds.
Then address white-fluid injury/recovery as a coherent family. Continue remaining
coverage and cross-facing consistency. Keep full goal active.
'''
    (ROOT/'docs/MARSH_SOUTH_COLLAPSE_MATERIAL_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
    print('Recorded dry source milestone; skill mirrors exact; full goal active/incomplete.')

if __name__=='__main__':main()
