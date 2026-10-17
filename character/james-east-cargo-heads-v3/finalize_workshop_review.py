from pathlib import Path
import json,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1]
review=json.loads((P/'workshop-review-evidence.json').read_bytes());assert review['failures']==0
review['visualReviewPending']=False;review['visualFindings']='All six clean actual room captures reviewed. Pickup/carry show crate in front and visible registered feet; North unload remains in front of workshop equipment with legs visible. Matte suit/head and original shared helmet are consistent in these captured poses. No continuous world-video or full-slot world-motion acceptance.'
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
atomic(P/'workshop-review-evidence.json',(json.dumps(review,indent=2)+'\n').encode())
selection=json.loads((P/'selection-evidence.json').read_bytes());selection.update({'actualTaskAcceptance':True,'actualTaskScope':'Default rotation0 salvage workshop; prescribed collision-clear approach and curiosity goal, actual actor-generated hauling route, initial bare/helmet, pickup/carry/unload six fresh-main disk checkpoints. Other rotations/natural scheduling/interruptions remain pending.','ordinaryRunSaveContinueAcceptance':True,'ordinaryRunSaveContinueScope':'Three workshop stages per initial gear; exact immediate actor/playback/pause/clock/source and normal completion. Not whole future trajectory equivalence.','actualWorkshopChecks':review['nativeChecks'],'actualWorkshopCapturesReviewed':6,'fullGoalComplete':False})
atomic(P/'selection-evidence.json',(json.dumps(selection,indent=2)+'\n').encode())
for mode in ['bare','helmet']:
    path=P/(mode+'-manifest.json');pack=json.loads(path.read_bytes());pack['status']='selected_default_workshop_context_validated_remaining_contexts_pending';atomic(path,(json.dumps(pack,indent=2)+'\n').encode())
section=f'''## James actual workshop cargo and disk Continue — October 2, 2026

Selected `character/james-east-cargo-heads-v3` exercised in default rotation0
salvage workshop with both initial gears. Prescribed collision-clear approach and
curiosity goal enter actual RoomActivity station, inspect/work/pickup, actor-generated
two-point hauling route, North unload and normal completion/next chooser.
Native{review['nativeChecks']}checks0fail; three ordinary RunSave disk writes/reads
and fresh main-scene restores per gear, six total. Immediate actor/playback/clock/
pause/source pixels exact at pickup/carry/unload; paused Continue stays fixed.
Normal curiosity relief exactly65 with ongoing.22/s need growth. No full future
world trajectory-equivalence claim. Engine0/no timeout; strict scratch whole owner
profile unchanged.10targeted dependencies and128selected source copy hashes remain
unchanged before separately recorded status-only metadata updates; broader main/
scene/library dependencies were not frozen. First run had2fixture failures from
expecting goal empty after completion: actual next chooser assigns another goal.
Fresh-main final-state probe diagnosed it; first run/guard/art retained. Only fixture
expectation/capture visibility changed; no gameplay/controller/raster fixes here.

All six clean actual room captures reviewed in workshop-world-review.png. Crate
stays in front during captured pickup/carry; feet visible, North unload in front
of workshop equipment. Matte suit/head/shared helmet consistent in captured poses.
Review-only card tray hiding removes UI obstruction. Main otherwise paused with
actual actor stepping; no natural scheduling, acquired gear, other layouts/rotations,
full cardinal turn matrix, all source slots in world or continuous movie acceptance.

Lesson: completion can clear an activity and choose another goal in the same
update; verify actual need relief/stage rather than requiring an artificial idle.
Read real state before altering assertions. World review must remove fixture UI
obstructions without changing room geometry or production interface preferences.
Player binary snapshots and source boards are distinct from ordinary RunSave/main
scene actor restoration. Next actual service-loss interruptions and remaining
turn/room contexts, West hand-edge cleanup and full master/material/proportion/
perspective/height/motion cross-family polish. Full James goal active/incomplete;
no final owner acceptance, commit or export.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes();assert section.splitlines()[0].encode() not in old;atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff=f'''# Project handoff

Updated: October2,2026 · Project: Brine Space · Task: James workshop cargo

## Objective and acceptance
Full James set/master/style/perspective/size/height/proportion/matte colour matching,
then cross-family consistency/polish. Full objective active/incomplete.

## Accepted decisions and constraints
Selected East cargo/connected-turn head corrections preserve original body/crate/
feet/clocks outside recorded head/collar rectangles; helmet unchanged. Native
fixtures isolate whole owner profile; no gameplay flags/room geometry changed.

## Current state
Selected paired9states/128refs. New native-workshop fixture verifies default0
actual RoomActivity inspect/work/pickup/generated hauling/unload for both gears.
Six fresh-main ordinary disk checkpoints. Clean six-capture board reviewed.
Initial wrong completion expectation diagnosed with fresh checkpoint probe and
corrected only in fixture; failure artifacts preserved. Five guides updated.

## Verification
{review['nativeChecks']}checks0fail,terminal0/no timeout,whole owner profile unchanged.
10targeted dependencies and128source hashes unchanged before status-only metadata
updates. Six immediate actor/playback/clock/pause/source restore equivalences and
normal65curiosity relief. Main otherwise paused/actor stepped. Not natural chooser
arrival, full future world trajectories, acquired gear or all cardinal/context motion.

## Next action
Actual service-loss interruptions and remaining turn/room contexts; West hand-edge
cleanup; remaining full set master/material/perspective/height/proportion/motion
and cross-family polish. No final owner acceptance, commit or export.
'''
atomic(P/'HANDOFF.md',handoff.encode());other=R/'character/james-side-motion-review-2026-10-02/HEAD_CANDIDATE_HANDOFF.md';atomic(other,handoff.encode())
print(json.dumps({'nativeChecks':review['nativeChecks'],'failures':0,'freshMainContinues':6,'capturesReviewed':6,'guidesUpdated':5,'fullGoalComplete':False}))
