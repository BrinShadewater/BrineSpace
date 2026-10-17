"""Record paired partial-seat mortality/Continue and existing seated regression."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent;R=P.parents[1]
O=R/'output/veld-lounge-partial-fall-north-native-v1';G=R/'output/veld-lounge-fall-north-native-v1'
n=json.loads((O/'validation.json').read_text());g=json.loads((G/'validation.json').read_text())
assert n['passed'] and g['passed']
records=json.loads((O/'records.json').read_text());assert len(records)==8
count=int(re.search(r'VELD PARTIAL LOUNGE NORTH FALL: (\d+) checks,0 failures',(O/'native.log').read_text())[1])
oldcount=int(re.search(r'VELD LOUNGE NORTH FALL: (\d+) checks,0 failures',(G/'native.log').read_text())[1])
heading='## Veld partial North lounge fall actual mortality and fresh Continue - October 2, 2026'
note=f'''
Staged character/veld-lounge-partial-fall-north-v1 opts into actual mortality via
loungeFallDeathMode=partial-north-v1. CrewSpritePlayer marks partial floor sources;
VeldDeathMotion requires dry matching gear/current North chair depth, lowering2 or
rising3, exact current source pixels against the candidate padded entry, registered
seat and fractional contact amount0.225..0.4. Source2 covers this partial interval;
other partial poses retain prior behavior. Exact displayed source/root/depth holds
180ms, chair offset holds to340ms then fades to zero520ms before original roll.
Saved four-field lounge registration binds finite vectors/contact amount/foot/root/
sort depth and specific source indices; foreign lounge fields rejected on other clips.
Normal loader admission unchanged; fixture loads only the new fall.

{count}native checks0fail/{n['seconds']}s,engine0/cleanlog. Eight actual RoomFlooding.kill
cases: lower/rise, two differing partial contact offsets, both gears. Eight ordinary
eligible RunSave disk writes/reads/fresh main-scene restore_staged;150reference+
150resumed20ms actor updates each=2400future steps. Independent source clock/root/
depth oracle,64malformed guards, unmarked and different marked entry rejection,
paused Continue, source/gear/foot/needs/timer/root/depth/corpse terminal equivalence.
Paired future native/source/master boards reviewed.12decoded source frames remain
exactly equal to preceding pre-integration contact captures: no new artwork change.
{n['targetedInputCount']}targeted inputs unchanged; broader dependencies not frozen.
Scratch APPDATA/all{n['realProfileFileCount']}owner non-log files unchanged.

Existing fully seated North regression: {oldcount}checks0fail/{g['seconds']}s,engine0,
eight actual mortality/fresh disk Continue cases and2400future actor steps, targeted
inputs and owner profile unchanged. Test scope is default lounge rotation0,
prescribed death API/stage/timer with actor-only future while main paused; not
natural hazard/chooser cadence, all rotations, title/new-process Continue or
continuous whole-world movie. Paid existing Bill ward wake/roster provides real
survivor/save eligibility; ward repair route itself not certified.

Lesson: preserve a partial furniture pose's actual fractional contact root instead
of promoting it to full sitting or zero floor offset. Bind the selected source
pixels as well as index/gear and retain registration after die() clears live state.
Reach floor root before rolling; exercise different offsets on the same source
through actual disk restoration and compare full future traces. Pixel/root tests
remain separate from master/native review and final owner acceptance.
Next remaining partial entrances, actual furniture contexts, normal paired bunk/
fall admission and natural world cadence; full cross-family polish remains open.
Full Veld goal active/incomplete. No commit/export requested.
'''
handoff=f'''# Project handoff

Updated:2026-10-02 - Project:BrineSpace - Task:Partial North fall mortality/Continue

## Objective and acceptance
Full master-matching Veld set/cross-family polish active/incomplete. New partial
North fall integration staged; normal admission and owner motion acceptance open.

## Accepted decisions and constraints
Selected exact partial lowering2/rising3 source, real fractional chair registration,
unchanged148/592ruler/artwork/master grade/native depth-pitch helmet/floor terminal.
Preserve physical navigation foot, owner furniture/layouts and normal save rules.

## Current state
CrewSpritePlayer/VeldDeathMotion partial opt-in/selector/finite root law/strict saved
bindings. Builder/manifests/validator updated;12frame pixels unchanged.
New test+UID/runner, eight future source/master/native boards, replay and evidence;
pipeline/bible/current status and both skill lesson copies updated.

## Verification
18builder/70package checks0fail. Native{count}checks0fail/{n['seconds']}s,8actual deaths,
8real eligible disk/fresh scene restores,2400future actor updates,64malformedguards,
exact entry/source/root/depth/gear/foot/timer/needs/corpse/paused continuity.
Existing seated regression{oldcount}checks0fail/{g['seconds']}s. Target inputs/owner
profile unchanged with scratch APPDATA. All paired future boards reviewed.
Scope rotation0 prescribed APIs/actor-only paused-main future; not natural world,
all layouts/rotations or title/new-process Continue. Broader dependencies not frozen.

## Next action
Remaining partial poses and actual furniture contexts, normal paired admission,
natural hazard cadence and full cross-family master/camera/scale/material polish.
No blocker, commit/export or final owner acceptance claim.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(P/'native-evidence.json').write_text(json.dumps({'native':n,'nativeChecks':count,'regression':g,'regressionChecks':oldcount,'records':8,'futureActorUpdates':2400,'malformedGuards':64,'artworkUnchangedAgainstPreviousContactCaptures':12,'normalSelection':False,'scope':'Rotation0 prescribed actual mortality and disk/fresh-scene actor future Continue'},indent=2)+'\n',encoding='utf-8')
for p in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(heading+'\n'+note+'\n'+t if p.name=='CURRENT_STATUS.md' else t.rstrip()+'\n\n'+heading+'\n'+note+'\n',encoding='utf-8')
print(f'{count} partial native/{oldcount} existing seated checks recorded; five lesson targets')
