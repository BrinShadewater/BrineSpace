from pathlib import Path
import hashlib,json,os,uuid
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
def atomic(path,data):
    t=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,path)
def write(path,data):atomic(path,(json.dumps(data,indent=2)+'\n').encode())
guards={name:json.loads((P/f'{name}-validation.json').read_bytes()) for name in ['validate','safety','admission']}
for g in guards.values():assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and g['profileDelta']==[]
inputs=json.loads((P/'runtime-input-before.json').read_bytes());after={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in inputs};assert after==inputs
native=json.loads((P/'native-evidence.json').read_bytes());safety=json.loads((P/'safety-evidence.json').read_bytes());views=json.loads((P/'review-evidence.json').read_bytes())
admission=json.loads((P/'admission-evidence.json').read_bytes())
assert native['failures']==0 and safety['failures']==0 and admission['failures']==0
selection={'status':'installed_reassignment_resume_native_verified_owner_review_pending','runtimeInstalled':True,'fullSetComplete':False,'newDrawings':0,'newSourceStates':0,'native':native,'safety':safety,'admission':admission,'profileGuards':guards,'runtimeInputHashes':after,'inputsStableDuringFinalInterval':True,'visualReview':views,'allFinalBoardsReviewed':True,'diagnostics':'First prescribed peer was present too early and claimed/completed the repair before James; timed-out proof retained before-peer-fixture-fix. Second proof rejected artificial recovered roster at disk admission; before-roster-fixture-fix retained. Final temporary peer admission is limited to synchronous reassign-to-Bill/reassign-to-James API calls before any peer update/claim/save; original roster restored. No Bill claim/service animation acceptance.','remaining':'Actual incoming other-worker handoff, other natural facings, physical floor loss, gear, ward/room families; cross-family/master/furniture/rotation/owner/export polish. Full animation goal active/incomplete.'}
write(P/'selection-review.json',selection)
for relative in ['character/james-hull-return-v1/selection-review.json','character/james-hull-lifecycle-v1/selection-review.json','character/james-repair-contact-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    path=R/relative;data=json.loads(path.read_bytes());data['hullReassignmentReview']='res://character/james-hull-reassign-v1/selection-review.json';write(path,data)
block=f"""## James reassigned hull repair resume — October 1, 2026

Installed scripts/james_hull_resume.gd/.uid: whole original pose entry from
neutral back to the exact saved paid-work pose. Reverse canonical source exit
recipe; no redraw, rescale, grade, progress reset or additional charge. Existing
paid work remains frozen during the short authored entry, then resumes normally.
Same-worker selection now returns success without releasing the actor/order.
Hull optional entry hook runs after existing travel/contact/hazard checks.
Branforth snapshot/restore/admission and grid renderer select source entry;
hull_return captures the actual current entry source for repeated cancellation
or reassignment. Critical hazards retain priority; sparks off during entry.

Final {native['checks']} native checks/0 failures, {views['captures']} captured views:
three actual paid North draw/held/stow repairs, exact same-worker no-op,
rapid reassign-to-Bill/reassign-back-to-James before any peer update/claim,
outgoing stow and neutral-to-original paid pose entry. Three paused real disk
Continues into fresh scenes during resumed entry: actor/player/pixels/room paid
progress/clock/pause exact. Physical foot and metal fixed through transitions;
normal paid progress resumes after exact original pose join. Temporary prescribed
peer admission only spans synchronous reassign calls; original roster restored
before updates/saves. This is not a Bill incoming-claim/service-animation proof.

Final {safety['checks']} safety/admission checks/0 failures: four actual North held
repairs, resumed entry interrupted by cancel/reassign/death/critical flood.
Exact first interrupted source, ordinary retraction, immediate death renderer,
flood priority, no stale effects. Nine saved corruption types each rejected,
including a canonical source recipe for the wrong paid target. Strict saved
recipe/elapsed/foot/duration/work fields; target must match original paid clock.
Additional {admission['checks']} source-clock/recipe/snapshot checks0failures:
180 prescribed samples across four bare facings/five budgets/nine phase seams,
ordinary renderer target exact and neutral/paid target source joins. This is
not other-facing physical job/Continue/visual acceptance. All three final
guards engine0/no timeout/scratch APPDATA/strict owner unchanged.
Seven frozen runtime/source inputs stable. All {views['captures']} final native and
selected whole-source captures reviewed: exact renderer RGBA hashes, original
matte grade, fixed148 ruler/p92,172, fixed screenshot foot486,362. Clean GIF uses
50ms per captured pose, simplified source order rather than real-time footage.
Water/vapor changes independently of body source pixels.

Retained diagnostic proofs: early artificial peer claimed/completed work;
then artificial recovered roster failed disk admission. Fixture now limits
prescribed peer presence to synchronous rapid reassignment, preserving normal
roster checks. No save-validator bypass or gameplay change to force a pass.
Lesson: completed paid progress determines the target pose, while entry owns
its own temporary clock. Preserve paid progress through both exits and entries;
never snap idle directly to an old work pose or restart paid work to hide it.
Selecting the current worker is a true no-op. Validate the canonical recipe
against the saved paid clock as well as the recipe's own source/index.
Actual other-worker claims/other facings/physical floor loss/gear, ward/room
and wider master/cross-family/furniture/rotation/owner/export polish remain.
Full animation goal active/incomplete. Evidence:character/james-hull-reassign-v1.

"""
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes();b=block.encode();atomic(path,b+old if path.name=='CURRENT_STATUS.md' else old+b'\n'+b)
handoff=f"""# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James reassigned hull resume

## Objective and acceptance
Full animation set and master/style/height/color consistency, then wider polish.
North bare reassignment/resume milestone; full goal remains active/incomplete.

## Accepted decisions and constraints
Whole selected matte source art, original paid progress and hazards retained.
Short entry holds paid work before resuming. Owner review pending; simplified GIF.
Preserve concurrent Bill/Veld work. No incoming Bill service acceptance claim.

## Current state
New scripts/james_hull_resume.gd/.uid; hooks in branforth_npc/hull_repair/
grid_canvas and current-source interruption handling in james_hull_return.
Same-worker reassignment preserves actor/order exactly. Evidence in this folder;
five guides updated and parent selections linked. No new drawings/state coverage.

## Verification
{native['checks']} native, {safety['checks']} safety/admission and
{admission['checks']} prescribed clock/recipe checks, zero failures. Other-facing
physical jobs remain unproven by the180 prescribed source samples.
Three fresh disk Continues; all {views['captures']} native/source views reviewed.
Exact source hashes, strict owner unchanged, seven frozen inputs stable.
Diagnostic fixture failures retained; prescribed temporary peer presence now
limited to synchronous API calls before any peer update/save. Not Bill claim.

## Next action
Actual other-worker handoff/other natural facings, physical floor loss, gear,
ward/room families, wider master/cross-family/furniture/rotation/owner/export.
"""
atomic(P/'HANDOFF.md',handoff.encode());print(json.dumps({'nativeChecks':native['checks'],'safetyChecks':safety['checks'],'captures':views['captures'],'guides':len(paths)}))
