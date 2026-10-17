from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-side-breathing-v1';C=R/'output/veld-seated-side-context-v1'
assert json.loads((O/'validation.json').read_text(encoding='utf-8'))['passed']
assert json.loads((C/'validation.json').read_text(encoding='utf-8'))['passed']
title='Veld side seated interruption and current room eligibility - October 1, 2026'
note=f'''## {title}

Staged East/West held breathing follow-up:361controlled native checks0failures,
25.12s engine0. Four interior phases per direction/gear give16controlled
interrupted_sit_rise_seconds cases: exact neutral rise entry, changed pixels only
inside bounded rear rib/sleeve, unchanged master head/helmet/collar/hardware/
hands/belt/hips/knees/boots and valid actor snapshots. Previous two-cycle player
clock/snapshot/native148-82 checks retained. No actual side service/furniture
or whole-scene Continue proof. No new source/grade/scale/runtime selection change.
162package/source checks from prior source interval remain scoped unchanged art.

Actual room eligibility:469checks0failures/71.27s engine0, fresh normal main
scenes, actual lounge/observation fixtures all four rotations, no artwork
injection or furnishing edits. Current lounge seated stations all North;
observation seated reading all South. No East/West sit/read eligibility in eight
current contexts. Eight native room crops reviewed, including moving lounge
furnishings across rotations. Both new native intervals preserve all2931owner
non-log files with scratch APPDATA. Evidence/context board:
output/veld-seated-side-context-v1. Paired UID scripts and isolated runners saved.

Lesson: a side approach to a chair is not a side-facing seated service. Verify
RoomActivity facing and current applied layout independently of authored pose
coverage; keep dormant side sources staged rather than inventing furniture or
changing accepted room/service behavior merely to install art. Controlled
breath relaxation proves protected pixels and source joins, not room contact.

Next actual gap: authored dry-collapse family remains unselected; its existing
role/world/Continue candidates omit bunk/seated/life entrances and have recorded
owner-profile guard deltas. Inspect actual selected seated/rest mortality source,
world offset and furniture depth before adoption, then clean normal-loader and
isolated disk lifecycle proof. Preserve those prior failed guard intervals;
do not label them clean because current unrelated seating guards pass.
Full Veld set and master/cross-family motion polish remain active/incomplete.
'''
for target in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]:
 old=target.read_bytes()
 if title.encode() not in old:
  data=note.encode('utf-8');target.write_bytes(data+b'\n'+old if target.name=='CURRENT_STATUS.md' else old+b'\n\n'+data)
handoff=P/'HANDOFF.md'
addition='''
## Current interruption/context follow-up - October 1, 2026
361controlled native checks0failures/25.12s:16interior side interruption hook
cases, only bounded breathing relaxes; exact neutral rise, protected master body,
snapshot admission. No actual side service/furniture/whole-scene Continue claim.
469current room eligibility checks0failures/71.27s:all four lounge/observation
rotations, no East/West seated eligibility. Lounge North/observation South;
eight actual room crops reviewed.2931owner non-log files unchanged in both
scratch intervals. Original313check interval archived by runner, source artwork
unchanged; native fixture extended, not a new art revision.
This supersedes the attempt to find default side furniture before adoption:
keep side sources staged/dormant, never invent furnishings to integrate art.
Next: selected seated/rest death entrances/world offset/depth and clean normal
dry-collapse integration/lifecycle, then full cross-family polish. Prior dry
candidate guard failures retain their scope. Full goal incomplete.
'''
if addition.splitlines()[1].encode() not in handoff.read_bytes():handoff.write_bytes(handoff.read_bytes()+addition.encode('utf-8'))
evidence=json.loads((P/'evidence.json').read_text(encoding='utf-8'))
for name in list(evidence['bindings']):
 path=R/name
 if path.is_file():evidence['bindings'][name]=hashlib.sha256(path.read_bytes()).hexdigest()
files=[f for f in P.iterdir() if f.is_file() and f.name!='evidence.json']
files += [f for folder in (O,C) for f in folder.iterdir() if f.is_file()]
files += [R/f for f in ['tests/test_veld_seated_side_breathing.gd','tests/test_veld_seated_side_breathing.gd.uid','tools/run_veld_seated_side_breathing.py','tests/test_veld_seated_side_context.gd','tests/test_veld_seated_side_context.gd.uid','tools/run_veld_seated_side_context.py','scripts/crew_room_activity.gd','rooms/full-wall-v1/default-layouts.json']]
for f in files:evidence['bindings'][f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
evidence['nativeChecks']=361;evidence['controlledInterruptions']=16
evidence['sideContext']={'checks':469,'failures':0,'seconds':71.27,'contexts':8,'sideEligibleStations':0,'artworkOverrides':False,'roomVisualReview':'all eight current default room crops reviewed'}
evidence['scope']='staged side source/player/controlled held interruption; current default room eligibility separately audited; no side furniture character-contact/service-loss/disk Continue/adoption proof'
(P/'evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'notes':5,'bindings':len(evidence['bindings']),'controlledChecks':361,'contextChecks':469,'goalComplete':False}))
