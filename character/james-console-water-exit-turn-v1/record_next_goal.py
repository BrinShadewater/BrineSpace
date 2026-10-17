"""Record the next-task continuity milestone without replacing shared notes."""
from pathlib import Path
import hashlib
import json
import os
import uuid

ROOT = Path(__file__).resolve().parents[2]
PACK = Path(__file__).resolve().parent
TITLE = 'James console-to-next-task turn continuity verified - September 30, 2026'

def atomic(path, content, before=None):
    if before is None:
        before = path.read_bytes() if path.exists() else None
    temporary = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    temporary.write_bytes(content)
    current = path.read_bytes() if path.exists() else None
    if current != before:
        temporary.unlink()
        raise RuntimeError(f'Concurrent edit: {path}')
    os.replace(temporary, path)

reports = {}
for name in ['native-next-goal', 'native-next-goal-restore', 'native-dry-equipment',
             'native-water-routes', 'test_npc_movement_trace',
             'test_npc_segment_clearance', 'test_owner_report_regressions']:
    report = json.loads((PACK / (name + '-validation.json')).read_bytes())
    assert report['exitCode'] == 0 and not report['timedOut'] and report['realProfileUnchanged'], name
    log = (PACK / (name + '.log')).read_text(encoding='utf8')
    assert not any(marker in log for marker in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:']), name
    reports[name] = report
journey = json.loads((PACK / 'native-next-goal-evidence.json').read_bytes())
assert journey['failures'] == 0 and len(journey['results']) == 8
assert all(not row['canceledTurns'] and not row['unfinishedTurnInterruptions'] for row in journey['results'])
turns = sum(len(row['turns']) for row in journey['results'])
evidence = {'checks': journey['checks'], 'journeys': 8, 'turns': turns,
            'canceledStarts': 0, 'unfinishedTurns': 0, 'reports': reports,
            'scope': 'Current normal next-goal chooser/update/player routes; seed17, four rotations, two water/gear cases. Native screenshots review initial turn slots only. Full goal remains active.',
            'postCheckSourceHashes': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in ['scripts/bill_npc.gd', 'scripts/branforth_npc.gd', 'scripts/grid_canvas.gd', 'tests/test_npc_movement_trace.gd']}}
atomic(PACK / 'next-goal-milestone.json', (json.dumps(evidence, indent=2) + '\n').encode())

handoff = f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James next-task turns

## Objective and acceptance
Continue James's full animation set and cross-family polish. This milestone verifies
normal console departure into the next task; it is not owner acceptance of the full set.

## Accepted decisions and constraints
Keep selected masters, matte material, anatomy and helmet/body registration. Existing
reversible-work authorization applies. No new raster, mirrored pose, layout, export or commit.

## Current state
`scripts/bill_npc.gd` holds the intended facing for each waypoint instead of deriving it
from rounded microsteps; optional validated `movement_heading` survives snapshots and
older saves remain readable. `scripts/branforth_npc.gd` includes the selected ordinary
turn envelope in empty-hand wet route clearance, using recorded family bounds plus the
four installed compact overrides. `scripts/grid_canvas.gd` checks all twelve selected
ordinary turns rather than the unrelated transition-action union. Conservative full-clip
checks remain during playback. Selected pixels and clocks are unchanged.

## Verification
Normal next task: {journey['checks']:,} checks, eight journeys, {turns} turns, no skipped
starts or unfinished turns. Actual disk restores: 57,746 checks/eight console journeys,
including moving egress. Dry equipment: 29,629 checks/192 cases. Furnished swimming:
2,036 checks/eight routes. Movement trace (including misleading rounded diagonal steps,
saved-heading validation and older snapshots), segment clearance and owner-report
regressions pass. All native runs serial, scratch APPDATA; real profile unchanged and
engine logs clean. Initial next-turn native screenshots reviewed in both gear modes;
they are contextual stills, not a complete visual review of all moving turn slots.

Preserved `prior-step-heading-*`, `pre-tail-envelope-*`, `tail-envelope-diagnostic-*`,
`pre-route-turn-envelope-*` and diagonal-failure logs record investigation, not acceptance.
Exact-start checks alone missed six mid-turn cancellations at275ms. A remaining-pose
union and current-pose-only gate did not resolve the route defect; those approaches
were removed. Waypoint-heading tolerance alone also failed the exact-diagonal regression;
the retained fix stores each segment's intended heading. Post-check hashes are snapshots,
not a claim of whole-file stability during concurrent unrelated actor work.

## Next action
Continue task-selector/traffic and full furniture, meals, equipment and exterior journeys,
including airlock return and mortality context. This fixture covers seed17 only and
does not establish every layout, destination, gear change or traffic interruption.
Full animation goal remains active; prior source coverage is not completion.
'''
atomic(ROOT / 'docs/JAMES_NEXT_GOAL_TURN_HANDOFF_2026-09-30.md', handoff.encode())

lesson = f'''\n### {TITLE}

Normal service completion must be followed into the next chosen task. Eight actual
console-to-next-task journeys ({journey['checks']:,} checks, {turns} turns) now have zero
skipped starts and zero incomplete finite turns. A start-only audit missed six turns
cut off at275ms. Dry equipment, furnished swimming and actual checkpoint restores
also pass; serial scratch profiles leave the owner profile unchanged.

Plan empty-hand wet edges with the exact selected turn envelope, including compact
overrides. Outgoing/destination locomotion profiles alone do not cover the middle pose;
a full pose can become blocked as the foot translates. Keep conservative playback
clearance after correcting the route. Testing only the rendered fallback pose can hide
the canceled transition. Compare prior active key/start/cycle with the next selection
to detect early interruption as well as skipped starts.

At large world coordinates, rounded microsteps can alternate their dominant axis.
Choose heading once per waypoint segment and retain it through motion and checkpoint
restore. Recomputing the remaining-vector heading or adding a tiny tolerance still
fails an exact-diagonal regression because rounding accumulates. Validate the optional
saved heading against the first waypoint and retain older-snapshot compatibility.

No raster, art density, grade or clock changed. Native next-turn stills are contextual
review only; traffic, other seeds/layouts and complete life/exterior journeys remain.
See docs/JAMES_NEXT_GOAL_TURN_HANDOFF_2026-09-30.md. Full James goal active.
'''
for relative in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md', 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
                 'skills/brinespace-character-pipeline/references/crew-consistency.md']:
    path = ROOT / relative
    before = path.read_bytes()
    if TITLE.encode() not in before:
        atomic(path, before + lesson.encode(), before)
mirror = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
before = mirror.read_bytes()
if TITLE.encode() not in before:
    atomic(mirror, before + lesson.encode(), before)
status = ROOT / 'docs/CURRENT_STATUS.md'
before = status.read_bytes()
if TITLE.encode() not in before:
    summary = f'''## {TITLE}

Normal console departure into the next chosen task passes {journey['checks']:,} checks:
eight journeys, {turns} turns, zero skipped starts or unfinished turns. Selected turn
envelopes now constrain James's empty-hand wet routes; shared movement retains waypoint
heading through rounding and save/restore. 57,746 restore, 29,629 dry-equipment and2,036
furnished-water checks plus three shared regressions pass. Clean native logs; scratch
profiles, real profile unchanged. Selected art/clocks unchanged; full goal active.
[Handoff](JAMES_NEXT_GOAL_TURN_HANDOFF_2026-09-30.md) records limits and next work.

'''
    atomic(status, summary.encode() + before, before)
print(json.dumps({'checks': journey['checks'], 'journeys': 8, 'turns': turns,
                  'reports': len(reports), 'fullSetComplete': False}))
