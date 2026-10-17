from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
native=json.loads((p/'actor-return-evidence.json').read_bytes());guard=json.loads((p/'actor-return-validation.json').read_bytes())
cases=[x for x in native['results'] if not x.get('diagnostic')]
assert native['checks']==961 and native['failures']==0 and len(cases)==6 and all(x['admitted'] and x['sameFoot'] for x in cases)
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert sum(len(x['trace']) for x in cases)==46
assert all(x['geometry']['footClear'] and (x['geometry']['envelopeClear'] or not x['geometry']['newDrawing']) for x in cases)
refs=json.loads((p/'reference-evidence.json').read_bytes());assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in refs['sources'])
def atomic(path,new):
 old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
path=p/'actor-return-review.json';review=json.loads(path.read_bytes());review.update({'visualReviewPending':False,'reviewed':'All46source/world changing poses in six boards inspected. Physical foot fixed, case returns to floor through captured existing actions, original shell retained. Torso/shoulder transition at new bridge entry is noticeable and needs continuous motion/master polish. Final floor-case/idle is not yet repaired.','continuousNativeMotionAcceptance':False,'completeReturnAcceptance':False});atomic(path,(json.dumps(review,indent=2)+'\n').encode())
(p/'second-actor-return-run/source-copy-scope.json').write_text(json.dumps({'scope':'Native second-run logs/evidence/fixture retained. Wrapper source copies were made after immediate priority-hook edits and are post-run copies, not a frozen tested input snapshot. Third/final run exercises current hooks through ordinary returns, but priority APIs themselves remain untested.'},indent=2)+'\n')
verdict={'selected':False,'fullGoalComplete':False,'actualPrescribedPowerLossSourceSegmentAcceptance':True,'completeReturnAcceptance':False,'cases':6,'checks':961,'nativeSourceWorldPosesReviewed':46,'needsRemainLive':True,'normalCancelledWorkReward':False,'candidateCheckpointAdmission':False,'normalSnapshotRejectsUnadmittedReturn':True,'realOwnerProfileUnchanged':True,'firstRun':{'checks':921,'failures':2,'reason':'Full envelope rejected unchanged terminal North unload sources in both gears. New pose geometry still requires envelope clearance; immutable already-drawn terminal hold only requires existing valid foot.'},'remaining':['Continuous native motion and noticeable torso/shoulder bridge entry polish.','Actual emergency/gear/death API priority validation; hook code exists but calls not exercised in this suite.','Explicit floor-crate and standing join.','Paired ordinary RunSave/fresh-main continuation and production admission.','Other cardinal/layout contexts, West tablet edges and full master/cross-family polish.']}
(p/'actor-return-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James actual workshop finite return candidate — October 2, 2026

Unselected return_actor.gd/return_player.gd with paired UIDs now exercise actual
workshop power loss at pickup, mid East/West turn carry and late North unload,
both initial gears. Shared normal NPC.update/needs/fire/flood run before its work
return hook; no full-actor suspension. Physical foot/path held only for finite
source segment. Displayed source key/index/gear is tracked exactly; selected
source plan drives grid drawing. Existing James clearance profiles explicitly
preloaded because subclass filenames otherwise trigger Bill lazy fallback.

Final native961checks0fail, six prescribed actual service-loss returns: pickup
320ms, carry2040ms, terminal unload80ms per gear.46changing source/world captures
reviewed in6boards. Exact first source and per-step native texture/oracle bindings,
planted foot, empty cancelled goal/path, live.22/s curiosity growth/no work reward
and finite completion pass. Candidate unsupported active snapshots explicitly
reject normal James validation instead of silently losing return state. No paired
save restoration/ordinary Continue or production selection admission yet.

First921checks2fail retained: full silhouette envelope rejected both unchanged
terminal North unload sources. No new source geometry was added there. Candidate
now permits finite immutable already-visible terminal hold at a valid foot;
changing return poses still require full source-union clearance (four cases pass).
Geometry decision recorded for all6cases. No furniture/layout changes. First run
scripts/log/guard/evidence and captures retained. Second run wrapper copies are
post-run copies, not frozen input evidence; scope note records this explicitly.
Third run includes immediate gear/death/render predicate hooks and corrected
immediate diagnostic field capture. Priority APIs themselves not exercised yet.

All46native poses reviewed: case remains in front through turn/bridge then lowers
to floor in captured existing action; original shell and physical contact retained.
New torso/shoulder entry change remains noticeable; continuous motion/master polish
and final floor-case/idle disposition unfinished. Captures are static changing-pose
coverage, not continuous native movie or natural whole-world scheduler acceptance.
Final engine0/no timeout; whole owner profile unchanged in scratch, six original
reference hashes unchanged at recording. No prelaunch broad input freeze.

Lesson: preserve normal needs/safety dispatch while holding ordinary movement.
Do not load a different actor's clearance profile through subclass filename fallback.
Separate new envelope growth from an immutable already-drawn hold. Refuse silent
partial checkpoints before lifecycle admission. Next priority API validation,
shoulder/hip/motion polish, floor-crate/standing and paired ordinary Continue;
remaining cardinal contexts/full master/cross-family James objective incomplete.
Evidence: character/james-cargo-return-bridges-v1/actor-return-acceptance.json and
actual-return-{bare,helmet}-workshop_*-review.png. Normal selection unchanged.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=path.read_bytes()
 if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James actual finite cargo returns

## Objective and acceptance
Full James master/style/perspective/size/height/proportion/matte set then
cross-family polish. Full objective active/incomplete; complete return pending.

## Accepted decisions and constraints
Retain selected art and original shell/pivots. Needs/safety dispatch stays live;
only ordinary movement held. Explicit James subclass clearance. No owner geometry
change; refuse unsupported candidate checkpoint rather than silently lose state.

## Current state
Staged actor/player with paired UIDs, candidate bridge/manifests, real workshop
power-loss fixture and46native changing poses. Pickup/carry/late unload source
segments work in both gears. Six native boards reviewed; five guides updated.
First failed run retained; static-terminal hold diagnosis corrected. Second archived
wrapper copies are post-run. Production still uses original controller selection.

## Verification
961checks0fail, six actual prescribed returns,46source/world poses reviewed.
320ms pickup/2040ms carry/80ms terminal per gear. Exact displayed start/source clocks,
planted foot, live needs/no cancelled reward, finite completion and unsupported
snapshot rejection. Four changing envelopes clear; two immutable holds add no new
geometry. Final engine0/owner profile unchanged scratch; original6refs hash-exact.
No paired return Continue, priority API tests, continuous native movie or natural
scheduling/all layouts/cardinals. No broad prelaunch dependency freeze.

## Next action
Priority API validation, noticeable torso/shoulder entry/hip motion polish,
floor-crate/standing handoff and ordinary save/restore lifecycle. Then production
admission, other cardinal/layout contexts and full master/cross-family polish.
West tablet hand edges remain open. No commit/export.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Six actual finite source returns and46native poses reviewed/recorded; complete return/priority/Continue remain pending; five guides updated.')
