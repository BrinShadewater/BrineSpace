from pathlib import Path
import hashlib,json,os,uuid
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
def atomic(path,data):
    t=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(data);os.replace(t,path)
def write(path,data):atomic(path,(json.dumps(data,indent=2)+'\n').encode())
guards={name:json.loads((P/f'{name}-validation.json').read_bytes()) for name in ['validate','safety']}
for g in guards.values():assert g['exitCode']==0 and not g['timedOut'] and g['realProfileUnchanged'] and g['profileDelta']==[]
inputs=json.loads((P/'runtime-input-before.json').read_bytes());after={p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in inputs};assert after==inputs
native=json.loads((P/'native-evidence.json').read_bytes());safety=json.loads((P/'safety-evidence.json').read_bytes());views=json.loads((P/'review-evidence.json').read_bytes())
assert native['failures']==0 and safety['failures']==0
selection={'status':'installed_cancellation_return_native_verified_owner_review_pending','runtimeInstalled':True,'fullSetComplete':False,'newDrawings':0,'newSourceStates':0,'native':native,'safety':safety,'profileGuards':guards,'runtimeInputHashes':after,'inputsStableDuringFinalInterval':True,'visualReview':views,'allFinalBoardsReviewed':True,'diagnostics':'Initial replacement expectation failed after late cancellation. An isolated real checkpoint probe confirmed the existing air-budget safety wait. Fixture corrected to assert that exact unclaimed/zero-progress state; gameplay unchanged. First evidence archived in before-replacement-probe. Probe guard exit0, strict owner profile unchanged.','remaining':'Actual other facings, reassignments/repeated cancellations, physical floor loss, gear and broader ward/room families; cross-family/master/furniture/rotation/owner/export polish. Full animation goal active/incomplete.'}
write(P/'selection-review.json',selection)
for relative in ['character/james-hull-lifecycle-v1/selection-review.json','character/james-repair-contact-v1/selection-review.json','character/james-torch-material-residue-v2/selection.json']:
    path=R/relative;data=json.loads(path.read_bytes());data['hullCancellationReview']='res://character/james-hull-return-v1/selection-review.json';write(path,data)
block=f"""## James cancelled hull repair return — October 1, 2026

Installed scripts/james_hull_return.gd: derive canonical whole-source retraction
from the currently selected draw/held/stow pose; reverse only drawn entry prefix,
or finish original stow suffix. Fixed physical foot and direction, no sparks.
Optional hooks in hull_repair/branforth_npc/bill_npc and grid_canvas select it
before ordinary job claim, after critical hazard handling. Original refund,
paid progress, auto-queue, duration and air-budget rules unchanged. Reassignment
hook is installed but native reassignment behavior remains unverified.
Strict saved recipe/source/index/elapsed/foot/timer/context validation. Fresh
Continue restores the same cancelled pose and paused clock. Unsafe contact,
foreign goal, helmet, expedition/locker and hazards invalidate the override.

Final {native['checks']} native checks/0 failures, {views['captures']} captured views:
three actual paid North cancellations at draw/held/stow, each with a paused
real disk Continue into a fresh scene. Exact first and neutral sources, fixed
foot, original refund and replacement charged once. Eligible replacement starts
at fresh entry; late replacement remains unclaimed at zero progress under the
original unsafe-air-budget rule. First fixture wrongly required every new job
to start; isolated saved checkpoint probe established intended safety waiting.
Failed first proof retained in before-replacement-probe; no gameplay change.
Final {safety['checks']} safety/admission checks/0 failures: actual held cancellation
followed by death/flood or prescribed foreign goal/helmet; nine snapshot
corruption types rejected in each. Immediate death renderer, flood priority.
Both final guards exit0/no timeout/scratch APPDATA/strict owner profile unchanged.
Seven relevant runtime/source inputs stable across final interval.

All {views['captures']} final captured native/source views reviewed on fixed-foot
boards. Original matte RGBA sources match renderer hashes; fixed148 ruler and
p92,172, no scale/grade edits. Clean GIF uses50ms per captured pose, simplified
source order, not continuous real-time footage. Water/vapor overlays vary
independently of source pixels in actual damaged-room views.
Lesson: finish from the current whole pose, defer job claim until neutral, and
distinguish animation completion from normal admission/safety waiting. Preserve
critical hazard priority, physical contact validity and exact saved source recipes.
Other natural facings, reassignments/repeated cancellations/physical floor loss,
gear, ward/room and cross-family/master/furniture/rotation/owner/export polish
remain. Full animation goal active/incomplete.

"""
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old=path.read_bytes();b=block.encode();atomic(path,b+old if path.name=='CURRENT_STATUS.md' else old+b'\n'+b)
handoff=f"""# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James hull cancellation return

## Objective and acceptance
Continue full James animation set and master/style/height/color consistency.
This milestone covers North bare cancellation return; full goal remains active.

## Accepted decisions and constraints
Whole selected matte source art, fixed foot, unchanged paid gameplay/safety.
Owner review pending; simplified GIF timing. Preserve concurrent Bill/Veld work.

## Current state
New scripts/james_hull_return.gd/.uid and optional hooks in branforth_npc,
bill_npc, hull_repair and grid_canvas. Evidence and fixtures in this folder.
Five guides updated; parent selections linked. No new drawings or state coverage.

## Verification
{native['checks']} native checks, {safety['checks']} safety/admission checks, all zero
failures; three real fresh Continues. All {views['captures']} final native/source
views reviewed; exact RGBA hashes. Strict owner profile unchanged. Seven input
hashes stable. Initial air-budget expectation failure and successful diagnostic
probe retained; fixture corrected without changing gameplay.

## Next action
Actual reassignment/repeated cancellation and other natural-facing coverage,
then wider gear/ward/room and cross-family/master/furniture/rotation polish.
Physical floor removal and release validation still pending.
"""
atomic(P/'HANDOFF.md',handoff.encode());print(json.dumps({'nativeChecks':native['checks'],'safetyChecks':safety['checks'],'captures':views['captures'],'guides':len(paths)}))
