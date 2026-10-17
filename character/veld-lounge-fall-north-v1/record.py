"""Scoped source/contact milestone; preserve concurrent notes byte for byte."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-lounge-fall-north-contact-v1'
package=json.loads((P/'package-checks.json').read_text());native=json.loads((O/'validation.json').read_text())
assert package['checks']==60 and package['failures']==0 and native['passed']
note='''## Veld North lounge fall source and chair audition - October 1, 2026

New staged character/veld-lounge-fall-north-v1 provides six finite seated fall
poses in both gears,12RGBA exports. Current lounge resolver chooses North in all
default rotations; East/West seating remains staged with no live service station.
Continue from actual North seat coverage rather than altering owner furniture
or inventing an East service. Exact entry matches selected North breathing0 and
coherent seated5; generated rear slump/knee brace then exact North roll/rest3..5.

Built-in imagegen exec-3a19c207-2db4-4a62-8f84-942fc81eefa7 retained raw and exact
prompt. Selected rear standing master is identity/material authority, selected
North seat is gesture, North floor source is landing choreography only. One
148/693 anatomical ruler; pooled skin/hair/science/neutral curves before resampling.
Rear skin uses explicit ear strips rather than brown scalp/face guesses. New
equipped poses reuse existing32x29 native40degree depth-pitch component, unchanged
body outside bounded head region. Rear rectangular vent, side ports, silver trim
and gasket remain consistent; no planar rotation used to invent depth pitch.
256x272/p128224/H148,finite1440ms,pooled source GIF palette and exact PNG alpha.

20builder/60independent package checks0fail; original-scale master board reviewed.
Native prescribed source/contact audition68checks0fail/42.9s,engine0/cleanlog.
Actual default lounge rotation0, clear resolver station, all12paired source poses
submitted to retained room renderer. Fixed physical foot; provisional root seats
entry/slump at rest, knee brace halfway to approach, roll/rest at clear floor.
Registered chair depth only for first2poses. Both full paired native/source boards
reviewed: figure visible in front of chair, landing clear of chair/plant. Captures
are discrete prescribed poses, not a natural continuous fall. First camera was
still settling; per-capture crop boxes retained rather than pretending same camera.
Scratch APPDATA/all2931owner non-log files unchanged; full dependency set not frozen.
First66s interval stopped on test-only void-loader return misuse, retained with
clean profile; corrected to check admitted frames and reran. No production script,
normal loader, mortality selector or furniture changes, no disk Continue proof.

Lesson: use current furniture-facing eligibility to prioritize source coverage.
Separate source design, provisional chair-root audition, actual mortality and
fresh-save continuation. Seated source calibration cannot certify a floor path;
actual submitted textures/contact/depth must be reviewed. Keep exact incoming
and existing landed bodies; match rear skin from anatomical ear pixels and reuse
real depth-pitch helmet components. Next opt-in North mortality registration and
strict saved selector/root validation, then paired full disk/future Continue.
Other cardinal lounge falls/partial seating, whole-world hazards, normal paired
bunk adoption and full cross-family master consistency/polish remain incomplete.
Full goal active; no commit/export or owner acceptance claim.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for i,path in enumerate(targets):
 old=path.read_bytes();payload=note.replace('\n','\r\n').encode('utf-8')
 if note.splitlines()[0].encode() not in old:path.write_bytes(payload+b'\r\n'+old if i==0 else old+b'\r\n'+payload)
handoff='''# Project handoff

Updated:2026-10-01 - Project:BrineSpace - Task:North lounge fall source/contact

## Objective and acceptance
Full Veld master-matching set and cross-family polish active/incomplete.
New North fall staged; production and final owner motion acceptance open.

## Accepted decisions and constraints
Actual default lounge chooses North; East/West source foundations remain staged.
Selected rear idle/seat authority, exact initial seat and existing floor3..5.
One148/693ruler, pooled rear-ear/semantic grade, native depth-pitch helmet.
256x272/p128224/H148,1440ms finite. Preserve owner furniture/normal selections.

## Current state
Raw sources/prompt, build/validate/review,12RGBAframes,two manifests/GIFs and
paired master board. New tests/test_veld_lounge_fall_north_contact.gd/.uid and
tools/run_veld_lounge_fall_north_contact.py. Native review/crops in this folder;
original captures/logs under output/veld-lounge-fall-north-contact-v1.
No production controller/loader/mortality changes. Five lesson records updated.

## Verification
20builder/60package checks0fail. Native68checks0fail/42.9s,engine0,cleanlog,
12actual room/source poses. Navigation foot fixed; provisional root amounts
1,1,.5,0,0,0 through LIFE.offset; first2poses use chair depth. Both native paired
boards and source/master board reviewed. Scratch/all2931owner files unchanged.
First66s void-loader test misuse failed/retained; corrected test rerun passed.
Discrete rotation0source audition only, not natural continuous death/Continue.
Camera settles after initial capture; crop boxes retained. Dependencies not frozen.

## Next action
Opt-in actual North seated mortality, exact displayed breathing/interior entry,
saved root/depth progression with strict validation. Full disk/fresh-scene future
Continue and actual native motion. Partial seating/other cardinal falls, whole-world
hazards, normal paired bunk adoption and complete Veld cross-family polish remain.
No commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
prompt=P/'sources/prompt-v1.txt';s=prompt.read_text(encoding='utf-8')
if 'Built-in result:' not in s:prompt.write_text(s+'\nBuilt-in result: exec-3a19c207-2db4-4a62-8f84-942fc81eefa7.png; raw retained as fall-v1.png.\n',encoding='utf-8')
files=list(P.glob('*.py'))+list(P.glob('*.json'))+list(P.glob('*.png'))+list(P.glob('*.gif'))+list(P.glob('*.html'))+[P/'HANDOFF.md',prompt,P/'sources/fall-v1.png',R/'tests/test_veld_lounge_fall_north_contact.gd',R/'tests/test_veld_lounge_fall_north_contact.gd.uid',R/'tools/run_veld_lounge_fall_north_contact.py',O/'native.log',O/'validation.json',O/'records.json']+list((P/'frames').rglob('*.png'))+list(O.glob('*-room.png'))+list(O.glob('*-source.png'))
files=[f for f in files if f.name!='candidate-evidence.json']
(P/'candidate-evidence.json').write_text(json.dumps({'generation':'built-in imagegen exec-3a19c207-2db4-4a62-8f84-942fc81eefa7','builderChecks':20,'packageChecks':60,'nativeChecks':68,'nativeSeconds':42.9,'normalSelection':False,'productionMortality':False,'diskContinue':False,'scope':'paired staged rear source with prescribed actual default-lounge contact audition; no natural continuous death proof','bindings':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('North source/contact milestone recorded in five lesson targets and concise handoff')
