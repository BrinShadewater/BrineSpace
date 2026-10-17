"""Record actual service dispatch and fresh disk restoration, with bounded scope."""
from pathlib import Path
import json,hashlib,re,shutil
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-north-continue-v1'
native=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text()
assert native['runtimePassed'] and '28 interruptions,6 fresh-scene disk restores' in log
count=int(re.search(r'VELD SEATED NORTH CONTINUE: (\d+) checks,0 failures',log)[1])
crops=json.loads((P/'continue-crop-review.json').read_text());assert len(crops['comparisons'])==6
equal=sum(item['roomCropEqual'] for item in crops['comparisons']);max_delta=max(item['maximumChannelDelta'] for item in crops['comparisons'])
archive=P/'revisions/pre-seated-continue-v1'
if not archive.exists():
    archive.mkdir(parents=True)
    for name in ['HANDOFF.md','STATION_REVIEW.md','candidate-evidence.json','index.html','station-review.html']:shutil.copy2(P/name,archive/name)
    (archive/'SCOPE.md').write_text('Earlier source/default lounge depth evidence and notes; not a complete byte rollback. Sources/frames unchanged. Failed snapshot fixture and prior incomplete first camera capture are retained in output/veld-seated-north-continue-v1/interval-before-*.\n')
title='Veld north seated interruption and fresh Continue — October 1, 2026'
guard='All2931non-log owner files unchanged.' if not native['realProfileChanges'] else 'Real profile delta observed, not attributed: '+','.join(native['realProfileChanges'])+'.'
note=f'''\n\n## {title}

Fixture-only paired north seated candidate exercised actual NPC update guard for
power loss and room suspension at six lowering phases plus settled seat, both
equipment variants:28interruptions. Actual service guard dispatches rise, clears
goal, retains displayed source pixels, contact/navigation foot and bounded chair
depth. Prescribed station entry, not natural chooser/routing or all hazard exits.

Six actual disk checkpoints (lower/held/rise x two gears), read and restored into
separately created main scenes via production RunSave.restore_staged. Candidate
overrides explicitly appended in each scene; no normal art selection. Exact
equipment/stage/action clock/pixels/contact/depth/paused persistence verified.
All six before/after native room/actor crops visually reviewed. {equal}are byte
equal; first bare lowering crop has broad small room-shade differences up to
{max_delta}/255 per channel despite exact source pixels/contact/depth. Cause not
proven, no whole-room pixel equality or renderer-shade continuity claim for it.
{count}checks,0failures,engine0/{native['seconds']}s/no errors. Scratch APPDATA.
{guard} Real selected architect Veld released through advance_core; no failure
or free-build switches, real save folder never used. No source/sprite/runtime edit
needed for this verification;60package/1184room pose/depth checks retain prior scope.

Failed first fixture omitted maintenance from four-key needs and correctly failed
actor/whole-checkpoint validation. Fixed only fixture, added immediate admission
guard; retained failed38.34s interval. Subsequent334checks/six restores passed,
but first before-camera captured preceding viewport despite valid retained source.
Retained that runtime-valid/visually-incomplete interval. New camera guard observes
actual world room center after frame_post_draw as well as retained source/depth;
latest full six-restore rerun supplies corrected camera before/after evidence.
Residual first-crop shade difference retained separately from camera registration.

Lesson: keep complete actor schema in full-save fixtures. Texture/slot readiness
does not prove deferred camera/scroll layout readiness after startup or Continue;
observe rendered viewport geometry, not a fixed sleep. Whole-window pixels can
differ in UI while registered room/actor crops and source state remain exact.
Next coherent held breathing, first-pair shade investigation, natural approach/exit/hazard routing and remaining
directional seated/life sources; rest/death joins and whole-set polish remain.
Full goal active/incomplete; candidate remains staged. No owner acceptance claim.
Handoff: character/veld-seated-north-coherent-v1/CONTINUE_HANDOFF.md.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/SKILL.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/SKILL.md')]:
    current=path.read_bytes()
    if title.encode() not in current:
        if path.name=='CURRENT_STATUS.md':path.write_bytes(note.lstrip().encode()+b'\n'+current)
        else:
            with path.open('ab') as out:out.write(note.encode())
handoff=f'''# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld north seated continuity

## Objective and acceptance
Full master-matched Veld set and whole-set polish remain active. North seated
pair has source/depth/contact, actual service-loss guard and fresh disk Continue
evidence. Held breathing, natural approaches/exits, hazard transitions, remaining
cardinal life sources and owner motion acceptance remain incomplete. Staged only.

## Accepted decisions and constraints
Master scale/materials/native helmet and all12sprite pixels unchanged. Optional
registered chair-front depth; preserve navigation and owner layouts. No normal
selection, free-build/failure toggles, owner save, commit/push/export change.

## Current state
New test_veld_seated_north_continue.gd/.uid and scratch runner. Actual selected
architect release, real lounge, actual update guard for power/suspend loss;
six real checkpoint writes/reads/fresh-scene staged restores with candidate
override in each independent scene. review_continue.py and native comparison
board/evidence retained. Earlier diagnosis/metadata under revisions/ and native
interval-before folders; historical recorder scripts must not overwrite current.

## Verification
{count}native checks,0failures,{native['seconds']}s engine0/no errors.28actual
service-guard interruptions;6fresh disk restores, exact source/stage/timer/gear/
navigation/contact/depth/paused persistence. All6before/after room crops reviewed;
{equal}byte equal. First bare lowering room crop shows broad small shade changes
up to{max_delta}/255 per channel, cause unproven; exact source/position/depth proven
but not exact whole-room shading for that pair. Scratch APPDATA; {guard}
Earlier60package/1184room pose/depth checks retain dated scope. First38.34s fixture
failed because maintenance need was omitted; corrected fixture only.334checks
then passed runtime but first camera-before frame remained stale; saved separately.
Latest fixture waits for actual post-draw camera and retained source/depth.
Shared grid_canvas.gd hash differs from preceding depth milestone; current Veld
seated member/helper path inspected and unchanged. Do not reinterpret older
native evidence as a proof of every concurrent shared renderer edit.
These tests prescribe chair entry; no natural chooser/routing, all hazard exits,
owner acceptance, exact first-pair room shading or changed-source breathing proof.

## Next action
Author coherent seated breathing against the retained final source; preserve
head/helmet identity, contact/scale/materials and loop seam. Then natural approach/
exit/hazard routes, remaining independent directional life sources, rest/death
joins and full cross-animation motion polish. Full goal remains incomplete.
'''
(P/'CONTINUE_HANDOFF.md').write_text(handoff)
(P/'HANDOFF.md').write_text(handoff)
index=P/'index.html';html=index.read_text().replace('Natural service-loss, fresh Continue and held breathing remain pending.','Actual power/suspension interruption and six fresh disk Continue checks now pass. Natural routing and held breathing remain pending.')
if 'continue-room-board.png' not in html:
    html=html.replace('<p><button', '<p><a href="../../output/veld-seated-north-continue-v1/continue-room-board.png">Actual before/after Continue comparisons</a></p>\n<p><button',1)
index.write_text(html)
page=P/'station-review.html';html=page.read_text().replace('Native contact, source ordering and interruption checks pass. Natural furniture routing, fresh Continue and held breathing still need review.',f'Native contact and source ordering pass. {count} checks cover actual power/suspension interruption and six fresh-scene disk restores. Natural routing and held breathing still need review. <a href="../../output/veld-seated-north-continue-v1/continue-room-board.png">Before/after Continue comparison</a>')
page.write_text(html)
registry=R/'tests/index.json';data=json.loads(registry.read_text());group=data['subsystems'].setdefault('veld-seated',[])
if 'test_veld_seated_north_continue' not in group:group.append('test_veld_seated_north_continue')
data['lanes']['test_veld_seated_north_continue']={'lane':'native','reason':'Actual power/suspend NPC guard and six real disk/fresh-scene candidate restores; explicit scratch APPDATA required.'}
registry.write_text(json.dumps(data,indent=2)+'\n')
old=json.loads((P/'candidate-evidence.json').read_text());paths={R/key for key in old['files']}
more=json.loads((P/'continue-evidence.json').read_text());paths.update(R/key for key in more['files'])
paths.update([P/'continue-evidence.json',P/'CONTINUE_HANDOFF.md',P/'record_continue.py'])
old.update({'continueChecks':count,'worldInterruptions':28,'freshDiskRestores':6,'continueRunner':native,'scope':'paired staged source/default lounge prescribed contact/depth, actual power/suspend NPC guard and six fresh disk staged Continue restores; no natural routing/held breathing/all hazards/owner acceptance','files':{path.relative_to(R).as_posix():hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}})
(P/'candidate-evidence.json').write_text(json.dumps(old,indent=2)+'\n')
print(json.dumps({'continueChecks':count,'boundFiles':len(paths),'normalSelection':False,'realProfileChanges':native['realProfileChanges']}))
