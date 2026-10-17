from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-lounge-early-fall-north-native-v1'
n=json.loads((O/'validation.json').read_text());p=json.loads((P/'package-checks.json').read_text())
assert n['passed'] and p['failures']==0
records=json.loads((O/'records.json').read_text());assert len(records)==8
count=int(re.search(r'VELD EARLY LOUNGE NORTH FALL: (\d+) checks,0 failures',(O/'native.log').read_text())[1])
heading='## Veld earliest North chair poses0and1 actual fall and fresh Continue - October 2, 2026'
note=f'''
New staged character/veld-lounge-early-fall-north-v1 completes specific floor-fall
coverage for selected North lowering poses0and1 and rising indices5and4. Exact
entrances plus established North standing-collapse interiors/terminal, transparent
bottom padding only:14PNG/24references. No new anatomy/ruler/grade/helmet design.
48builder/{p['checks']}package and original-source binding/alpha checks0fail.

CrewSpritePlayer early-north-v1 opt-in and VeldDeathMotion bind actual dry matching
gear/North chair depth, exact current source pixels, registered station, selected
source pose and contact interval0..0.1 (pose0) or0.1..0.225 (pose1).
Exact displayed whole source/root/depth held180ms. Small fractional chair root
then blends to zero340ms before floor brace; saved root/depth survives die() clearing
live furniture state. Strict saved source/gear/first/finite-vector/range/physical
foot/root/sort bindings and rejection of foreign lounge fields retained.
Normal loader admission unchanged; all North fall candidates remain staged.

Native{count}checks0fail/{n['seconds']}s,engine0/cleanlog.8actual RoomFlooding.kill
cases (early poses0and1 lower/rise, both gears),8ordinary eligible RunSave disk
writes/reads/fresh main-scene restore_staged;150reference+150resumed20ms steps each
=2400future actor updates, independent source clock/root/depth oracle.64malformed
guards, unmarked/different marked entry rejection; exact paused Continue/source/
position/depth/foot/timer/gear/needs/corpse terminal equivalence.16existing/boundary
selector checks with all North candidates loaded: partial/held/final/late falls,
plus lowering/rising zero-contact endpoints. These are capture-selection guards,
not another full previous-family disk replay. All8paired future native/source/
master boards reviewed: visible chair contact, attached body, consistent matte
materials/native rear helmet, clear landing.112future room/source presentations;
entry/restore captures retained. Replay uses actual source/root traces, not a
continuous native world movie.

{n['targetedInputCount']}targeted inputs unchanged; broader dependencies not frozen.
Scratch APPDATA/all{n['realProfileFileCount']}owner non-log files unchanged. Scope
rotation0 prescribed death API/stage/timer, actor-only future while main paused;
not natural chooser/hazard cadence, all layouts/rotations or title/new-process
Continue. Existing paid Bill ward wake supplies real survivor/save eligibility;
repair worker/route itself not certified.

Lesson: standing/first knee-bend entrances can reuse an established standing fall,
preserving exact incoming source and fractional furniture registration. Blend even
a small root to floor instead of snapping it away when the first interior begins.
Guard zero-contact endpoints and existing selectors with all candidate families
present; then compare actual saved future motion against masters/room contact.
All6North lowering/rising sources and held North breathing now have staged specific
falls with dated native evidence. Next normal paired North fall admission and
broader real-world furniture/hazard cadence, paired bunk admission/remaining actual
contexts, full-library master/material/perspective/size/proportion polish.
Full Veld goal active/incomplete; no commit/export or owner final acceptance claim.
'''
handoff=f'''# Project handoff

Updated:2026-10-02 - Project:BrineSpace - Task:Earliest North chair fall/Continue

## Objective and acceptance
Full master-matching Veld set/cross-family polish active/incomplete. All six North
chair-transition source poses now have staged specific fall coverage, not normal
runtime admission or final owner motion acceptance.

## Accepted decisions and constraints
Reuse established ground-collapse body/material/native rear helmet without grade
or rescaling. Exact incoming selected pose and real fractional chair root; preserve
physical foot, furniture/owner layouts and ordinary save rules.

## Current state
New pack14padded PNG/24references, builder/validator/source binding/previews.
CrewSpritePlayer/VeldDeathMotion early opt-in/finite root law/strict saved binding.
New test+UID/runner, eight future source/native/master boards/replay/evidence;
five lesson targets updated. Normal loader unchanged.

## Verification
48builder/{p['checks']}package/{count}native checks0fail, native{n['seconds']}s/engine0.
8actual mortality/8real eligible disk/fresh-scene restores/2400future actor steps,
64malformed guards,16existing/zero-contact endpoint selection checks. All8paired
future boards reviewed. Target inputs and owner profile unchanged/scratch APPDATA.
Scope rotation0 prescribed APIs/actor-only paused-main future; not natural world,
all rotations/title/new-process Continue. Broader dependencies not frozen.

## Next action
Normal paired North fall admission and broader real-world chair/hazard cadence,
paired bunk admission/remaining contexts and full cross-family master/style/camera/
scale/material polish. No blocker, commit/export or owner final acceptance claim.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'native-evidence.json').write_text(json.dumps({'native':n,'nativeChecks':count,'package':p,'records':8,'futureActorUpdates':2400,'malformedGuards':64,'existingAndBoundarySelectorGuards':16,'normalSelection':False,'scope':'Rotation0 prescribed mortality/disk/fresh-scene actor-future Continue'},indent=2)+'\n')
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 t=path.read_text(encoding='utf-8')
 if heading not in t:path.write_text(heading+'\n'+note+'\n'+t if path.name=='CURRENT_STATUS.md' else t.rstrip()+'\n\n'+heading+'\n'+note+'\n',encoding='utf-8')
print(f'{count} native checks/8cases and five lesson targets recorded')
