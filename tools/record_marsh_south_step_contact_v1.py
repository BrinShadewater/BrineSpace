"""Record the actual normal contact failure, whole registration and scoped evidence."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'character/marsh-v2/supplemental/south-step-contact-v1';REVIEW=BASE/'world-review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=REVIEW/'verification.json';r=json.loads(p.read_text())
for b in r['boards']:assert sha(REVIEW/b['file'])==b['sha256'];b['actuallyInspected']=True
assert sha(REVIEW/r['comparison']['file'])==r['comparison']['sha256'];r['comparison']['actuallyInspected']=True
r['visualScope']='First full native station image, whole before/after registration board, all six route/restore comparison boards (44pairs) and failed/corrected before-after inspected. Static sampled images; no continuous cadence acceptance.'
r['contactLimit']='Strict supporting sole depth invariant verified in selected room on four prescribed routes. Bottom-row sole-center horizontal range.88184world units pretransfer reflects varying sole shape/registration; no complete2Dplant/contact or all rooms/rotations/autonomous/task acceptance inferred.'
r['normalAdmissionReceiptSha256']=sha(BASE/'admission.json')
p.write_text(json.dumps(r,indent=2)+'\n')
latest=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json';current=json.loads(latest.read_text())
current['heldReviewEvidence']={'previousInventory':'character/marsh-selected-normal-audit-2026-10-03-post-south-step-detail/inventory.json','previousInventorySha256':sha(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-step-detail/inventory.json'),'unchangedStates':227,'revisedState':'walk-step-south','verification':p.relative_to(ROOT).as_posix(),'verificationSha256':sha(p),'scope':'Every other selected state unchanged; revised seven-pose source and actual normal controller/render submissions inspected with strict supporting-depth proof. Whole-frame Y+1 retains all drawing pixels. No full motion/detail/contact/set acceptance.','fullGoalComplete':False}
latest.write_text(json.dumps(current,indent=2)+'\n')
note='''
## Marsh South short-step normal contact correction — October 3, 2026

Actual normal actor/main/grid/catalogue study of the revised South step exposed
what the prior50source/player checks did not cover. Four prescribed5/5.7341/6/7world
unit routes in default furnished cold_store,20ms actor updates, normal paid/failure
flags false-free-build/false-disable-failures. No private controller/source loading
or StudyMain draw offset. Observational arrival-count subclass calls normal super.
Uncorrected V1:874checks,24strict supporting-depth failures,176samples/44captures,
6actor-only binary restores. Sole in phase3 was1sourcepixel high (.44108world unit).
Other checks passed;5314bounded inputs/2931owner files stable,terminalexit1. Failure
retained. Prior narrow player passing did not certify physical contact.

The error was uniform registration, not anatomy/density/detail. Whole revision02
frame translatedY+1 into identical184square canvas. Bottom outgoing row alpha0;
every surviving RGBA row equals original previous row; visible count identical.
No clipping, interpolation, painting, head/limb splice, scale or pivot metadata
change. Corrected supporting sole restores original source depth; crown shifts1px
as a consequence of whole registration, not a fitted head. Normal overlay:
character/marsh-v2/supplemental/south-step-contact-v1,only walk-step-south slot3.
Six other drawings/state metadata and227other states exact.228states/1190slots/
89normal body manifests. No new generation/runtime/gameplay/resource/room/save
changes. Previous unregistered revision retained for provenance, not final selection.

Corrected V2 normal actor/main/grid:874checks/0failures,176samples/44exact source/
native pairs,6actor-only topology rebuild restores, pause holds and single finite
arrival per route.5319bounded inputs/2931owner non-log files unchanged,engineexit0,
no ERROR/WARNING/SCRIPT ERROR. First full native capture, whole registration board,
all six source/native route/restore boards and failed/corrected comparison actually
inspected. Whole supporting-depth invariant is verified only for prescribed room/
routes. Horizontal bottom-row sole center varies.88184world units pretransfer;
foot-shape centroid is not a complete2Dcontact proof. No continuous cadence,
autonomous route/task selection, every room/rotation, disk fullRunSave/TitleContinue
or full visual-polish acceptance inferred. Actual paid building not exercised;
room/site insertion is fixture setup. Root/controller/main renderer unchanged.

Latest source inventory character/marsh-selected-normal-audit-2026-10-03-post-south-contact/
inventory.json. Native evidence output/marsh-animation-audit/south-step-normal-world-v2-2026-10-03;
failed V1 namespace retained. Both native sessions terminal. No browser activity,
commit/export. Full Marsh goal remains active with broader native seams, master/
detail/material/camera/grade consistency, natural behavior and save/Continue open.

Lesson: a1pixel sole drift admitted after a silhouette/detail check can break a
physical supporting-foot invariant. Measure actual controller draw position and
sole during every authored hold, preserve failed evidence, distinguish vertical
support depth from complete2Dcontact. A demonstrated uniform offset may be fixed
by exact whole-frame registration only after proving no visible clipping; do not
rescale the body or patch a foot. Re-run the same invariant, not a looser tolerance.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for q in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with q.open('rb') as f:f.seek(max(0,q.stat().st_size-100000));tail=f.read().decode('utf-8',errors='ignore')
    if '## Marsh South short-step normal contact correction' not in tail:
        with q.open('a',encoding='utf-8') as f:f.write(note)
installed.write_bytes(canonical.read_bytes())
print('24contact failures retained;whole Y+1 correction passes874checks;44native/source pairs reviewed;pipeline/bible/status/skill recorded')
