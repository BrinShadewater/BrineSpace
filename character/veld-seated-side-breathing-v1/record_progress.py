from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
O=R/'output/veld-seated-side-breathing-v1';N=R/'output/veld-read-north-context-v1'
native=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert native['passed'] and json.loads((N/'validation.json').read_text(encoding='utf-8'))['passed']
note='''## Veld side seated breathing and current North reader context - October 1, 2026

Staged/unselected veld-seated-side-breathing-v1: independent fitted East/West
neutral005 bodies, both gears, 24RGBA exports/four states, six600ms phases per
3.6s loop. Bounded rear rib/lower sleeve deformation uses measured North maximum
0.363636px. Premultiplied interpolation prevents transparent-edge colour bleed;
no mirrored body, new anatomy, per-pose scale, translation or grade. Head/hair/
helmet/collar/chest fittings/science badges/cuffs/hands/belt/hips/knees/boots
retain exact neutral RGBA. Actual blue patch fringe excluded from moving mask.
Source head/helmet already fitted to directional master; no new head replacement.
162package checks0failures,32deterministic bound outputs; protected regions,
neutral loop seam and actual down/rise source joins exact. Side helmet source
collar differs from bare through y144; paired body equality starts at y145,
while each complete protected head/collar retains its own original source.

313controlled native checks0failures/24.77s/engine0: actual Veld held getter
over two visual-clock cycles in four gear/facing cases, exact neutral joins,
calibration/contact marker, player snapshot admission and same-clock restore.
Native148/82 drawing and24paired source poses/detail, full four-clip browser
page reviewed. No actual furniture/service-loss/disk Continue/normal selection
or owner motion acceptance claim. All2931owner non-log files unchanged using
scratch APPDATA. Initial native313check trial had6fixture failures: original
helmet profiles were loaded after bare held override changed one slot to six.
Fixed paired load order; source artwork/runtime unchanged. Repeated rows in
first native review corrected to show all four cases; failed interval archived.
Lesson: validate each original paired profile before overriding paired held
slots; controller held loops use production visual-clock getter, not finite
frame_at_elapsed terminal clamping. Source protection is not furniture evidence.

North observation context completed:241checks0failures/40.36s/engine0, actual
main/default geometry and stations in all four rotations, no artwork injection.
Old wooden-desk/chair-rear hidden by current default layouts; modern South
sofa/read station exists in all four, North reader station absent. Pure old
empty-furniture fallback still returns North point(0,112) without rest_point.
Four current room captures reviewed;2931owner non-log files unchanged/scratch
APPDATA. This supersedes the proposed default North desk-contact integration:
keep North reader staged as dormant fallback, do not invent furniture or change
accepted layouts merely to make that source eligible. No North character-contact
or lifecycle proof. Evidence: output/veld-read-north-context-v1.

Remaining: valid side furniture/service contact and interruption/Continue before
adoption, North lounge selection lifecycle, inherited rest/death and broader
master/cross-family motion polish. Full animation goal active/incomplete.
Handoff/evidence: character/veld-seated-side-breathing-v1.
'''
targets=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for target in targets:
 old=target.read_bytes()
 if note.splitlines()[0].encode() not in old:
  addition=note.encode('utf-8')
  target.write_bytes(addition+b'\n'+old if target.name=='CURRENT_STATUS.md' else old+b'\n\n'+addition)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 1, 2026. Project: BrineSpace. Task: Veld side seated breathing.

## Objective and acceptance
Complete the full master-consistent Veld set, then cross-family polish. This
milestone adds independent paired side held breathing; full goal incomplete.

## Accepted decisions and constraints
Exact fitted East/West neutral005, fixed256canvas/p128224/H148; no mirror,
grade or regenerated heads. Measured North0.363636px maximum,600ms x6. Only
rear rib/lower sleeve y150:162 changes; actual blue patch pixels excluded.
Existing helmet collar differences through y144 preserved; body paired y145+.

## Current state
New build/verify,24RGBA frames/four states/two manifests/four GIFs/contact/index,
registration/source bindings; native fixture+UID and isolated runner added.
Staged/unselected; production loader/actor/furniture unchanged.
North context test+UID/runner and four default-room captures prove no eligible
North reader station in current defaults. North reader remains dormant/staged.

## Verification
162package checks0failures,32deterministic outputs.313native checks0failures,
24.77sec, two actual held cycles/both facings/gears, neutral joins/calibration,
player snapshot/same-clock restore and148/82 rendering. Source detail/contact,
native board and full browser page reviewed. All2931owner non-log files unchanged.
First native interval313checks6failures from fixture load order preserved in
output archive; corrected paired load order, no source/runtime workaround.
North context241checks0failures/40.36s; four room crops reviewed. Evidence hashes
recorded after runs; dependency interval stability unmeasured.
No actual side furniture/service loss/disk Continue or owner acceptance claim.

## Next action
Prove valid independent side furniture contacts/lifecycle before adoption;
continue North lounge selection lifecycle and inherited rest/death joins, then
full-set perspective/proportion/grade/detail/motion polish. Do not add a North
desk to current observation defaults just to integrate staged art.
''',encoding='utf-8')
target=R/'character/veld-read-seated-north-coherent-v1/HANDOFF.md'
correction='''
## Current default context audit - October 1, 2026
241native checks0failures/40.36s, actual observation default geometry/stations
all four rotations: legacy wooden desk/rear chair hidden, modern South sofa/read
present, North read station absent. Four native room crops reviewed.2931owner
non-log files unchanged/scratchAPPDATA. Pure missing-furniture fallback North
(0,112) has no rest_point. Previous default North desk integration next-action
is superseded: keep reader staged/dormant; never invent furniture or edit owner
layouts for eligibility. No North character-contact/lifecycle acceptance.
Evidence: output/veld-read-north-context-v1. Continue independent side breathing,
North lounge selection lifecycle and remaining rest/death/master polish.
'''
if correction.splitlines()[1].encode() not in target.read_bytes():target.write_bytes(target.read_bytes()+correction.encode())
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='evidence.json']
files += [f for folder in [O,N] for f in folder.iterdir() if f.is_file()]
files += [R/f for f in ['tests/test_veld_seated_side_breathing.gd','tests/test_veld_seated_side_breathing.gd.uid','tools/run_veld_seated_side_breathing.py','tests/test_veld_read_north_context.gd','tests/test_veld_read_north_context.gd.uid','tools/run_veld_read_north_context.py','rooms/full-wall-v1/default-layouts.json','scripts/crew_sprite_player.gd','scripts/grid_canvas.gd','scripts/veld_npc.gd','scripts/crew_room_activity.gd']]
reg=json.loads((P/'registration.json').read_text(encoding='utf-8'))
files += [R/f for f in reg['sourceBindings']]+[R/reg['amplitudeAuthority']]
bindings={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'evidence.json').write_text(json.dumps({'bindings':bindings,'scope':'staged side source/player/controlled held Veld; actual current North default room eligibility distinct; no side furniture/service/whole-scene Continue/adoption proof','nativeChecks':313,'nativeFailures':0,'northContextChecks':241,'northContextFailures':0,'visualReview':'24source phases/detail, all four gear/facing cases native148/82, browser full page; four current observation room crops','intervalStability':'hashes after run; dependency interval stability unmeasured'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'notes':len(targets),'evidenceBindings':len(bindings),'goalComplete':False}))
