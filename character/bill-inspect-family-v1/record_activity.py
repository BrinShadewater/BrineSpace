from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
OUT=ROOT/'output/bill-inspection-activities-v1';REG=ROOT/'output/bill-inspection-regression-v1'
native=json.loads((OUT/'validation.json').read_text());regression=json.loads((REG/'validation.json').read_text())
assert native['passed'] and regression['passed'] and not native['realProfileChanges'] and not regression['realProfileChanges']
assert '1454 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill standing reader service integration

## Objective and acceptance
Complete Bill's full master-consistent animation set, then cross-animation polish.
Standing inspection art and service draw/loop/stow are now normally installed.
The full goal remains active; this is an integration milestone.

## Accepted decisions and constraints
24states/144refs; shared256plane/pivot128,224/H148/dry depth0; native master helmets.
Source matte/detail/size grading remains unchanged.480ms draw/stow,960ms loop.
Original cold-store6s,workshop2s,equipped meal6s/drink3s service clocks remain.
Sealed helmets use the reader; bare meals and other actors retain their behavior.

## Current state
scripts/bill_inspection.gd derives poses from saved service timer, never cosmetic
time. BillNPC/CrewLife/normal grid renderer select draw/loop/stow. At arbitrary
loop-to-stow boundaries, retain the displayed whole source pose for first60ms.
Power loss cancels goal and reverses partial draws or completes remaining stow;
inspection_return_pose is snapshot validated/default-1 and restored. Untouched
zero-length draws clean up; floating boundary return timers clamp to480ms.
No new economy rule, actor selection, art generation or service duration change.
Both manifests and ACTIVE_ASSETS retain normal family selection.

## Verification
80source checks; prior1,036 normal selected pixel/metadata/idle-join checks.
1,454 actual-service/native checks pass42.10s: five physical station/gear cases
(cold-store bare/helmet,workshop bare/helmet,galley helmet), all service phases,
240 power-loss entry/loop/stow boundary cases over scripted four directions,
25actual RunSave disk round trips and exact selected pose/contact restoration.
Normal drink transition/completion checked; full drink-specific boundary matrix
is not separately covered.15actual room draw/loop/stow images and native82 timeline
board retained; representative cold-store/workshop/galley loops visually reviewed.
Five targeted regressions pass128.83s,including72 room/rotation/actor service
cases and48 actual approaches. All2,914 owner non-log files unchanged in both
scratch-profile runs. Native evidence is not autonomous all-direction contact proof.
Source candidate fixtures' old cosmetic elapsed=-1 assumption predates the new
saved service clock; current activity fixture is authoritative for runtime timing.

## Next action
Audit selected inspection silhouettes against real contacts in all room rotations,
with interruption/restore contact invalidation and hazard takeover. Add dedicated
equipped drink boundary coverage. Then replace bare meals, generic rest and dry
death; finish full-set material/proportion/pacing polish,including remaining2–3px
source interior motion variation. Keep provenance and source/native/runtime scopes
separate; no full-set completion claim. No commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill standing reader service integration — September30,2026.
Selected24states/144refs now drive actual cold-store/workshop/equipped meal draw,
inspection loop and stow from saved service timers. Original6/2/6/3s clocks stay;
bare meals/other actors unchanged. Power loss cancels goal and retains exact
entry/loop/stow pose; partial reverse/remaining return and cached pose survive save.
1,454native checks PASS42.10s: five physical station/gear services,240scripted
cardinal boundary cancellations,25actual disk round trips,15room renders/native82
timeline. Representative three rooms reviewed;5regressions PASS128.83s including
72room/activity cases and48approaches. Scratch profiles preserve2,914owner files.
Lesson: activity timers own loop phase as well as finite transitions. Preserve the
actual last loop pose at stow, clamp floating boundary durations, and explicitly
clean zero-time cancelled draws. Keep generated recovery wards paired with the
site layout in disk-checkpoint fixtures. Broader world contact/clearance/hazard
and dedicated drink boundary evidence remain, followed by meals/rest/drydeath and
full-set polish. Full goal active. Handoff: character/bill-inspect-family-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill standing reader service integration — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','bare-manifest.json','helmet-manifest.json','verification.json','HANDOFF.md','index.html']]+[ROOT/name for name in ['scripts/bill_inspection.gd','scripts/bill_inspection.gd.uid','scripts/bill_npc.gd','scripts/crew_life.gd','scripts/grid_canvas.gd','tests/test_bill_inspection_activities.gd','tools/run_bill_inspection_activities_validation.py','tools/run_bill_inspection_regression.py']]+[OUT/'validation.json',OUT/'native.log',OUT/'loaded-water-carry.png',REG/'validation.json',REG/'regression.log']+list(OUT.glob('*-loop.png'))+list(OUT.glob('*-draw.png'))+list(OUT.glob('*-stow.png'))
(P/'candidate-evidence.json').write_text(json.dumps({'status':'selected_runtime','checks':{'package':80,'selected_renderer':1036,'actual_service_native':1454,'targeted_regressions':5},'states':24,'refs':144,'native':native,'regression':regression,'scope':'normal source selection and actual service clocks/interruptions/25disk restores; wider contact/clearance/hazards and full-set polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded Bill reader service integration and remaining full-goal work')
