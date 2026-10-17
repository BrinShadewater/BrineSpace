from pathlib import Path
import hashlib
import json
import os
import uuid
P = Path(__file__).resolve().parent
R = P.parents[1]
TITLE = 'James real locker approaches and fitting journeys verified - September 30, 2026'

def atomic(path, content, before=None):
    if before is None:
        before = path.read_bytes() if path.exists() else None
    temp = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(content)
    if (path.read_bytes() if path.exists() else None) != before:
        temp.unlink()
        raise RuntimeError('Concurrent edit: ' + str(path))
    os.replace(temp, path)

for name in ['native-locker', 'test_branforth_crew', 'test_station_systems']:
    report = json.loads((P / (name + '-validation.json')).read_bytes())
    assert report['exitCode'] == 0 and not report['timedOut'] and report['realProfileUnchanged'], name
    log = (P / (name + '.log')).read_text(encoding='utf8')
    assert not any(marker in log for marker in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:']), name
data = json.loads((P / 'native-locker-evidence.json').read_bytes())
assert data['failures'] == 0 and len(data['results']) == 8
assert all(row['arrivalHeading'] == 'east' and len(row['samples']) == 12 and row['nextTicks'] > 0 for row in data['results'])
data['scope'] = ('Normal AirlockService discovery/request, native main crew update/vitals/movement, '
                 'four actual dry airlock rotations, eight fit/remove transitions and eight next-task '
                 'journeys. Every selected slot, east arrival heading, shelf marker, exact endpoint '
                 'master, grounded contact, completion gear and first moving gear/walk frame asserted. '
                 'Current standard layouts and seed17 only; arbitrary layouts, crowded lockers, '
                 'refill, service interruptions and disk restore remain separate.')
fixture = P / 'native-locker.gd'
before = fixture.read_bytes()
old_scope = b'Normal AirlockService locker discovery/request, native main crew update/vitals/movement and selected frame clock across four actual airlock rotations; full twelve slots each fit/remove. Next task, arbitrary layouts, service interruptions and disk restore separate. Arrival heading diagnostic, not asserted.'
if old_scope in before:
    atomic(fixture, before.replace(old_scope, data['scope'].encode()), before)
atomic(P / 'native-locker-evidence.json', (json.dumps(data, indent=2) + '\n').encode())
proof = {'checks': data['checks'], 'transitions': 8, 'slots': 96, 'nextTaskJourneys': 8,
         'fullSetComplete': False, 'postCheckSourceHashes': {
             name: hashlib.sha256((R / name).read_bytes()).hexdigest()
             for name in ['scripts/bill_npc.gd', 'scripts/branforth_npc.gd', 'scripts/grid_canvas.gd']}}
atomic(P / 'milestone.json', (json.dumps(proof, indent=2) + '\n').encode())
selection_path = R / 'character/james-helmet-fitting-east-v1/selection.json'
before = selection_path.read_bytes()
selection = json.loads(before)
assert selection['runtimeInstalled']
selection['limitations'] = ['Normal production locker discovery/request and routing verified across four standard airlock rotations. Other layouts, crowded lockers, refill, interruptions and fitting disk restore remain separate.']
selection['productionLockerJourneys'] = {
    'evidence': 'character/james-locker-journeys-v1/native-locker-evidence.json',
    'checks': data['checks'], 'transitions': 8, 'selectedSlots': 96,
    'nextTaskJourneys': 8, 'arrivalFacing': 'east',
    'review': 'Agent-reviewed actual locker endpoints/lift and middle fitting pose in all four rotations; earlier owner art acceptance retained.',
    'fullSetComplete': False}
selection['next'] = 'Equipment interruption/restore and full furniture, meal and exterior journey polish; full James goal active.'
atomic(selection_path, (json.dumps(selection, indent=2) + '\n').encode(), before)

handoff = f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James actual equipment locker

## Objective and acceptance
Continue James's full animation set and consistency goal. Earlier owner acceptance of
the selected fitting artwork remains; this is agent-verified journey integration.

## Accepted decisions and constraints
Keep the selected 12 authored fitting poses/exact reverse removal, 2.14/2.24s clocks,
shared helmet, master endpoints, body density, matte grade and grounded registration.
Existing reversible-work authorization applies. No raster, room layout, export or commit.

## Current state
`scripts/bill_npc.gd` offers a nullable locker-route hook; other actors retain their
default route. James's `scripts/branforth_npc.gd` override uses a collision-clear fine
connector west of the exact shelf contact and retains headings during smoothing.
Already-contacting east-facing James stays at contact for the return action. Coarse
graph-only facing failed beside the chamber/wall; no contact or obstacle was moved.
Selected fitting metadata now removes an obsolete staged limitation and records current
production-discovery/route proof. Native fixture, logs, captures, review builders and
`native-review.gif` live in `character/james-locker-journeys-v1`.

## Verification
{data['checks']:,} checks/zero failures: four actual airlock rotations, eight normal
AirlockService fit/remove requests,96 selected timeline slots, eight normal seed17
next-task arrivals. Main crew update/vitals/safety and actual movement run; all traveled
legs clear, arrival already east, fitting contact stationary, shelf handoffs correct,
gear commits only at completion, exact idle masters and correct first walking gear.
James three-crew and station-system regressions pass. Serial scratch APPDATA, clean
logs, real profile unchanged. Native bare/equipped endpoints, lift and all four rotated
locker contexts reviewed; body stays matte and grounded. Peak189px alpha height includes
the lifted helmet and is not a body-height ruler. Review exports confirmed LFS-filtered.

Baseline `prior-approach-*` found north/north/south/west arrivals snapping east. Failed
heading assertions and graph-only candidate intervals retained. First capture was
clipped into the HUD; `initial-camera-incomplete.png` and prior evidence retained.
Current capture waits for the entire review region to lie inside the station viewport;
all final crops are complete. Post-check source hashes are snapshots, not an assertion
of whole-file stability during concurrent unrelated actor work.

## Next action
Prove equipment service interruptions, actual fitting checkpoints/Continue, refill and
crowded or other-layout lockers. Continue furniture/meals and full exterior/airlock-return
journeys plus all-family master/style/height/grade comparison. Full goal remains active.
'''
atomic(R / 'docs/JAMES_LOCKER_JOURNEY_HANDOFF_2026-09-30.md', handoff.encode())
lesson = f'''\n### {TITLE}

Actual locker discovery and fit/remove movement now pass {data['checks']:,} checks:
four rotations, eight transitions/96 timeline slots and eight next-task arrivals.
Normal shelf markers, stationary contact, exact master joins and first walking gear
are asserted. Native endpoints/lift and all four rotated contexts reviewed; selected
pixels, material, body density and clocks unchanged. Existing owner acceptance retained.

An authored action facing is an arrival requirement. The previous nearest graph point
produced north/north/south/west arrivals before snapping east. Between-node contact beside
a wall/chamber can lack a facing-aligned graph point. Use a clear local connector to the
existing exact contact and preserve its heading when smoothing; do not move furniture
or contact to make the test pass. Already-contacting correct-facing actors need no trip.

Lifted equipment increases whole-alpha height (189px here); measure anatomy against
master rulers rather than rescaling the held item and body to a standing silhouette.
Source/frame validation is distinct from a visible real locker handoff. Native capture
must wait for observable viewport containment; the first successful save cropped the HUD
instead of the actor. Current stills/GIF use complete viewport-contained native crops.

Serial scratch tests preserve the owner profile. Other layouts/traffic, interruption,
refill and fitting checkpoints remain separate. See
docs/JAMES_LOCKER_JOURNEY_HANDOFF_2026-09-30.md. Full James goal active.
'''
for path in [R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             R / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before = path.read_bytes()
    if TITLE.encode() not in before:
        atomic(path, before + lesson.encode(), before)
status = R / 'docs/CURRENT_STATUS.md'
before = status.read_bytes()
if TITLE.encode() not in before:
    section = f'''## {TITLE}

James now approaches the real locker facing east, removing north/south/west arrival
snaps. Clear fine connector preserves exact shelf contact and selected fitting art.
{data['checks']:,} native checks pass four rotations/eight transitions/96 slots and eight
normal next-task journeys; exact master joins, shelf handoffs and committed moving gear.
Two shared regressions pass; clean logs, scratch profiles and owner files unchanged.
Native endpoints/lift/rotated contacts reviewed; skills/pipeline/bible updated. Equipment
interruptions/restore and full life/exterior work remain; full goal active.
[Handoff](JAMES_LOCKER_JOURNEY_HANDOFF_2026-09-30.md).

'''
    atomic(status, section.encode() + before, before)
print(json.dumps(proof))
