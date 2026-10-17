from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-lounge-late-fall-north-native-v1'
n=json.loads((O/'validation.json').read_text());assert n['passed']
p=json.loads((P/'package-checks.json').read_text());assert p['failures']==0
records=json.loads((O/'records.json').read_text());assert len(records)==8
count=int(re.search(r'VELD LATE LOUNGE NORTH FALL: (\d+) checks,0 failures',(O/'native.log').read_text())[1])
heading='## Veld late North lounge poses3and4 mortality and fresh Continue - October 2, 2026'
note=f'''
New staged character/veld-lounge-late-fall-north-v1 covers exact selected late
lowering poses3and4 and matching rising indices2and1. Four padded entry PNGs,
24manifest references: the established authored North seated slump/brace/roll/rest
are reused directly, with no new anatomy, rescaling, grading or helmet change.
Source joins reviewed beside the prior selected North seated/standing materials.
28builder/{p['checks']}package/source binding/alpha checks0fail.

CrewSpritePlayer late-north-v1 opt-in marker; VeldDeathMotion requires current dry
matching gear/North chair-contact metadata, exact selected entry pixels and actual
registered station. Contact ranges0.4..0.6 for pose3 and0.6..0.8 for pose4.
Exact whole source/root/depth holds180ms; seat root holds360ms then fades to zero
720ms, preserving existing authored seated-fall law. Four-field saved lounge root
binds finite local foot/seat/depth/amount, entrance index/gear/first/offset/sort depth
and physical foot. Foreign lounge fields rejected for other clips. No normal
loader admission. Existing source2/fully seated selectors remain unchanged.

Native{count}checks0fail/{n['seconds']}s,engine0/cleanlog:8actual RoomFlooding.kill
cases (pose3/pose4 lowering/rising, both gears),8ordinary eligible RunSave disk
writes/reads/fresh main-scene restore_staged;150reference+150resumed20ms steps
each=2400future actor updates. Independent source clock/root/depth oracle,
64malformed guards and unmarked/different-marked-source rejection, exact paused
Continue/source/root/gear/foot/timer/needs/corpse terminal match. Six existing
partial/held/final-seat capture-selection regression checks with all candidates
loaded together. These selector guards are not a new full old-family disk replay.
All8paired future native/source/master boards reviewed;112future room/source
presentations plus entry/restore captures. Native chair contact remains visible,
landing clear; original body/material/rear helmet retained. Replay derives from
captured source/root traces, not continuous world video.

{n['targetedInputCount']}targeted inputs unchanged; broader dependencies not frozen.
Scratch APPDATA/all{n['realProfileFileCount']}owner non-log files unchanged. Scope
default lounge rotation0/prescribed death API/stage/timer, actor-only future while
main paused; not natural chooser/hazard cadence, all rotations or title/new-process
Continue. Paid existing Bill ward wake supplies ordinary survivor/save eligibility;
ward repair route itself not certified.

Lesson: a new entrance does not require new collapsed anatomy when the selected
partial posture already joins an established master-matching slump. Keep exact
entry pixels and fractional chair registration, bind candidate to source pose,
then test forward and reverse choreography through actual save/future playback.
Direct references preserve accepted material and hardware without another grade
or rescale pass. Shared-folder presence alone does not prove a selector is active.
North poses2..5/held now have staged specific falls; earliest poses0and1, normal
paired admission, other actual furniture contexts, natural world cadence and
full cross-family polish remain open. Full goal active/incomplete; no commit/export.
'''
handoff=f'''# Project handoff

Updated:2026-10-02 - Project:BrineSpace - Task:Late North seated fall joins

## Objective and acceptance
Full master-matching Veld set/cross-family polish active/incomplete. Late North
poses3and4 now have staged actual mortality/Continue proof, normal admission open.

## Accepted decisions and constraints
Exact selected entrances; reuse established authored slump/landing and native
rear helmet, no rescaling/new grade. Preserve actual fractional chair registration,
physical foot, owner furniture/layouts and ordinary save rules.

## Current state
New pack4padded entrances/24references, builder/validator/source previews/boards,
source bindings. CrewSpritePlayer/VeldDeathMotion late opt-in and strict saved
source/root bindings. New test+UID/runner, eight future native/master boards/replay;
five lesson targets updated. Normal loader unchanged.

## Verification
28builder/{p['checks']}package and{count}native checks0fail/{n['seconds']}s,engine0.
8actual deaths/8real eligible disk+fresh-scene restores/2400future actor updates,
64malformed guards and candidate opt-in/pixel-binding checks. Six existing capture
selector regression checks; not a full old-family disk replay. Eight future paired
boards reviewed. Targeted inputs/owner profile unchanged with scratch APPDATA.
Scope rotation0 prescribed APIs/actor-only paused-main future; no natural world,
all rotations/title/new-process Continue. Broader dependencies not frozen.

## Next action
Earliest seated poses0and1, normal paired bunk/fall admission, actual furniture
contexts/natural hazard cadence, full cross-family master/camera/material polish.
No blocker, commit/export or final owner acceptance claim.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'native-evidence.json').write_text(json.dumps({'native':n,'nativeChecks':count,'package':p,'records':8,'futureActorUpdates':2400,'malformedGuards':64,'existingSelectorRegressionChecks':6,'normalSelection':False,'scope':'Rotation0 prescribed actual mortality/disk/fresh-scene actor-future Continue'},indent=2)+'\n')
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 t=path.read_text(encoding='utf-8')
 if heading not in t:path.write_text(heading+'\n'+note+'\n'+t if path.name=='CURRENT_STATUS.md' else t.rstrip()+'\n\n'+heading+'\n'+note+'\n',encoding='utf-8')
print(f'{count} native checks/8cases and five lesson targets recorded')
