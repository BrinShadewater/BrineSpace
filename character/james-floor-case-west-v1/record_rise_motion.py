from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'motion_rise_v4-evidence.json').read_bytes());guard=json.loads((p/'motion_rise_v4-validation.json').read_bytes());review=json.loads((p/'motion-rise-v4-review.json').read_bytes());inputs=json.loads((p/'motion_rise_v4-inputs.json').read_bytes())
assert data['checks']==659 and data['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
motion=[x for x in data['results'] if x.get('motion')];assert len(motion)==2 and all(x['midpointSamples']==4 for x in motion)
assert review['losslessApngDecodedChecks']==180 and len(inputs)==22
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review.update(visualReviewPending=False,reviewed='All90 chronological source/native room pairs inspected in six boards. Paired authored midpoint splits original crouch/standing jump with grounded registration. Remaining original-standing to idle changes case hardware/boot overlap. No continuous browser playback watched, full-motion/normal selection/Continue acceptance incomplete.',continuousPlaybackWatched=False,fullHandoffAccepted=False)
atomic(p/'motion-rise-v4-review.json',(json.dumps(review,indent=2)+'\n').encode())
acceptance={'selected':False,'fullGoalComplete':False,'nativeChecks':659,'failures':0,'actualPrescribedCarryPowerLossReturns':2,'nativePairsReviewed':90,'midpointSamplesPerGear':4,'midpointHoldSeconds':0.08,'losslessApngRgbDurationChecks':180,'targetedInputsUnchanged':22,'ownerProfileUnchanged':True,'originalReleaseIndex':4,'originalSourcesPreserved':True,'caseDuplicateAtMidpoint':False,'ordinaryWestUnloadSourceBankOverriddenInFixture':True,'ordinaryWestUnloadActorExecutionTested':False,'normalSelectionChanged':False,'fullHandoffAccepted':False,'remaining':['Original terminal standing to idle changes case hardware/boot overlap.','New7-frame bank checkpoint binding and floor-art revision not admitted.','Normal action path, actual normal disk/title Continue, full return and natural scheduling pending.','V9 collar/head turn and full cardinal/master/cross-family polish.']}
(p/'rise-motion-acceptance.json').write_text(json.dumps(acceptance,indent=2)+'\n')
section='''## James West paired rise exercised in native return — October 2, 2026

Staged7-frame unload-West manifests preserve original0..4, insert paired V4
midpoint at5/80ms, retain original standing5 at6/70ms. Shared planner consumes
actual bank; source-release remains original exact hash/index4. New fixture
floor-state validates7-frame shape; prior6-frame lifecycle/checkpoint unchanged.
Existing embedded-case lookup recognizes midpoint in unload bank automatically.
Overrides available to ordinary source player, but ordinary West actor unload
execution not exercised here; no normal selection or save schema admission.

Two actual carry power-loss returns/both gears,45native20ms samples each.
659checks0fail/engine0/owner profile unchanged; midpoint displayed4samples each,
owned fixed case and no duplicate prop. Finite return completes, first departure
23.9234world units; fixed camera includes ground/case contact. All90source/native
room pairs visually inspected in six boards. Four lossless APNGs/180decoded
RGB/duration checks pass;22targeted prelaunch inputs unchanged, not recursive
world dependency freeze. Final600ms is viewer-only hold, repeat resets excerpt.
Continuous browser playback not claimed; technical pass not full motion acceptance.

Rise registration/pose progression improved from original one-step jump. Remaining
terminal standing->idle hardware/boot overlap changes: full handoff NOT accepted.
Do not equate split crown spacing with complete anatomy/colour/master acceptance.
Lesson: inserting into the actual unload source bank preserves planner row clocks
and lets existing embedded-case suppression cover new pose; exact cue identity
must remain validated, and bank-shape/save bindings need a deliberate revision.

Next consistent separate case/body-only standing/idle contact, floor-art and7-frame
checkpoint binding, full return/ordinary unload/native replay, normal disk/title/
new-process Continue, V9 collar/head turn and all cardinal/master/cross-family work.
Evidence:character/james-floor-case-west-v1/rise-motion-acceptance.json,
motion_rise_v4-evidence.json,motion-rise-v4-review.json. Goal active/incomplete.
No normal selection, commit/export or full-set acceptance.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West rise/prop seam

## Objective and acceptance
Full James set matching directional masters/style/camera/height/proportions/matte
grade, then cross-family polish. Incomplete; staged candidate unselected.

## Accepted decisions and constraints
Exact original endpoints/cue4/owner profile/normal loader/geometry preserved.
V4 paired midpoint, common p128224/H148; no individual pose height normalization.

## Current state
New paired7-frame unload manifests, rise_floor_state/actor/player and pairedUIDs,
motion_rise_v4.gd,22input hashes/evidence/log/guard, six reviewed boards/four APNGs.
Midpoint80ms lies between exact original4/5. Source-release remains index4;
existing renderer suppresses separate case for midpoint. Old checkpoint not revised.
Normal selection untouched. Five guides updated; no commit/export.

## Verification
659native checks0fail/two actual power-loss returns/both gears;4midpoint samples
each.90source/room pairs reviewed,180APNG RGB/duration checks;22hashes unchanged.
Engine0/owner unchanged; first ordinary departure23.9234units. Fixed camera,
20ms sampled updates; viewer600ms terminal hold, no continuous playback claim.

## Next action
Case hardware/boot overlap still changes at standing->idle; resolve single case
and body contact. Bind new bank/floor-art revision into staged checkpoint, replay
full return/ordinary action; normal disk/title/new-process Continue; V9 collar/head
turn; full cardinal/master/cross-family passes. Full goal active/incomplete.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Native paired rise milestone recorded;90pairs reviewed; five guides/HANDOFF updated; incomplete.')
