# Historical recorder: superseded by record_dry_installation.py; do not rerun.
from pathlib import Path
import json, uuid

P = Path(__file__).resolve().parent
R = P.parents[1]

def verified(pack, name, summary):
    report = json.loads((pack / (name + '-validation.json')).read_text())
    log = (pack / (name + '.log')).read_text()
    assert report['exitCode'] == 0 and not report['timedOut'] and report['realProfileUnchanged']
    assert 'SCRIPT ERROR:' not in log and '\nERROR:' not in log and summary in log

verified(P, 'native-routes', '12947 checks; 0 failures; 192 actual goal/movement cases')
verified(R / 'character/james-arrival-facing-polish-v1', 'native-installed', '3793 checks; 0 failures')
verified(R / 'character/james-water-family-v1', 'native-installed-routes', '2036 checks; 0 failures; 8 installed real routes')
e = json.loads((P / 'route-evidence.json').read_text())
services = [x for x in e['results'] if x['variant'] == 'installed' and x['service']]
assert len(services) == 46 and sum(x['stopSlots'] for x in services) == 276
assert all(x['arrivalClip'] == 'swim-stop-north' and x['finalClip'] == '' for x in services)
assert all(not x['genericStopAllowed'] and x['selectedStopAllowed'] for x in services)
w = json.loads((R / 'character/james-water-family-v1/installed-route-evidence.json').read_text())
assert w['failures'] == 0 and all(x['arrived'] for x in w['results'])
assert all('swim-start-' + x['initialFacing'] in x['seenClips'] and 'swim-stop-' + x['initialFacing'] in x['seenClips'] for x in w['results'])

def atomic(path, change):
    before = path.read_bytes() if path.exists() else b''
    after = change(before)
    if after == before:
        return
    tmp = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'') != before:
        tmp.unlink()
        raise RuntimeError('Concurrent edit: ' + str(path))
    tmp.replace(path)

selection = json.loads((P / 'selection.json').read_text())
selection.update(status='installed_wet_workstation_facing_and_stops', checks=e['checks'],
    stopServices=46, stopSlots=276, genericArrivalRegressionChecks=3793,
    waterRouteRegressionChecks=2036, fullSetComplete=False,
    pending=['Connected-room life-support service approaches', 'Dry workstation transitions',
             'Complete furniture/meal/equipment/exterior journeys',
             'Nonblocking East maintenance prop rectangle overlaps need full journey visual review'])
atomic(P / 'selection.json', lambda _: (json.dumps(selection, indent=2) + '\n').encode())

note = '''### James selected straight water transitions installed - September 30, 2026

The combined transition envelope includes turns from other directions: it rejected
all46 reached workstation stops although the selected straight-stop frames fit.
Keep the conservative turn envelope. For James straight start/stop only, normal
grid now checks the complete selected clip's alpha bounds against existing swim
geometry. Player records per-frame bounds from the CPU image during PNG load;
metadata survives CanvasTexture equipment loading. Bounds retain actual pivot and
65.28/standingHeight density, union every clip slot, fail closed if unavailable.
No smaller body, blocker bypass, pose warp, art/clock/grade change or save field.

12,947 clean native checks/192 paired route cases PASS:46 service stops,276 authored
slots, paused pixel holds and finite treading joins; all44 old services retained.
Eight selected82px rows reviewed,24 real equipment captures retained and10 reviewed.
3793 generic arrival regression checks PASS. 2036 ordinary-water route checks PASS:
eight actual furnished cross-room routes show all four starts/stops in both modes,
200 selected-pose envelope samples clear navigation blockers. Four East initial
samples overlap a nonblocking maintenance prop's art rectangle; two native views
reviewed, no whole-journey prop acceptance claimed. The stale water fixture compared
all actions against an old catalog: only later salvage/cargo entries differ.
Preserve failure evidence; assert all eight ordinary transition entries and unchanged
swim/tread profiles rather than unrelated later action families. Final logs clean,
owner profiles unchanged. Life-support service approaches, dry equipment and full
life/exterior journeys remain. Full James goal active.

'''
for path in [R / 'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',
             R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
             R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
             R / 'skills/brinespace-character-pipeline/references/crew-consistency.md',
             Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(path, lambda b: b if note.encode() in b else b + b'\n' + note.encode())

headline = '''## James wet equipment stop transitions installed - September 30, 2026

James now plays the selected straight stop at all46 reached workstations. Full clip
bounds fit where the old combined turn envelope did not. 12,947 route/stop checks,
3793 generic-arrival and2036 eight-route water regression checks PASS; native pose
and equipment views reviewed, profiles unchanged. No art or clock changes.
Connected-room life support, dry equipment and full journeys remain; James goal active.
[Handoff](JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md).

'''
atomic(R / 'docs/CURRENT_STATUS.md', lambda b: b if headline.encode() in b else headline.encode() + b)
handoff = '''# Project handoff

Updated:2026-09-30 Ã‚Â· Project:Brine Space Ã‚Â· Task:James equipment arrival continuity

## Objective and acceptance
Full James animation/master consistency and complete cross-family journeys.
Wet station approach facing and selected straight stops installed; full goal active.

## Accepted decisions and constraints
Keep master density/material and full body clearance. Equipment governs facing.
Do not force transitions through props or shrink the body. Preserve public override
interfaces and unrelated concurrent source edits. Owner visual acceptance pending.

## Current state
Previous bill_npc/branforth_npc route-facing hook retained. crew_sprite_player.gd
records full alpha extent metadata at PNG load and exposes selected clip union.
grid_canvas.gd uses it for James straight starts/stops; turns and other actors keep
their checks. No art, clocks, layouts, saves or grade changed. Native route fixture
now verifies all stop slots and captures real equipment. Ordinary-water fixture
asserts its eight transition keys instead of unrelated newer action envelopes.
Evidence/selection/recorders in character/james-workstation-arrival-polish-v1.
Pipeline, bible, current status and both consistency skill copies updated.
Do not rerun either historical recorder; record_stop_installation.py is current.

## Verification
12,947 clean checks PASS,192 baseline/installed actual chooser/movement cases.
All44 prior services retained;46 now reach services;38 facing snaps become0.
All46 selected stop envelopes fit,276 slots play and pause exactly, then tread.
Eight82px selected frame rows and10 of24 native equipment captures reviewed.
3793 generic arrival checks PASS;2036 ordinary-water checks PASS,8 real furnished
routes show four-direction starts/stops,200 selected envelopes clear navigation.
Four East starting samples overlap nonblocking prop art rectangles; two native views
reviewed. These are not whole-prop/traffic/journey acceptance. Stale whole-actions
fixture failure retained and scope corrected from explicit catalog differences.
All final logs clean, real profiles unchanged, no native process running.

## Next action
Prove connected-room life-support service approaches; this seeded192-case matrix
reaches no life-support station in either variant. Then dry equipment transitions,
complete furniture/meal/equipment/exterior journeys and cross-family material/
motion review. Preserve full goal; source coverage and finite fixtures are not
full owner or release acceptance.
'''
atomic(R / 'docs/JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md', lambda _: handoff.encode())
print('Recorded selected straight water transitions:46 stops/276 slots; full goal active.')
