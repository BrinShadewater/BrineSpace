from pathlib import Path
import json
import os
import uuid

P = Path(__file__).resolve().parent
R = P.parents[1]
TITLE = 'James normal crew-traffic turn journeys verified - September 30, 2026'

def atomic(path, content, before=None):
    if before is None:
        before = path.read_bytes() if path.exists() else None
    temp = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    temp.write_bytes(content)
    if (path.read_bytes() if path.exists() else None) != before:
        temp.unlink()
        raise RuntimeError('Concurrent edit: ' + str(path))
    os.replace(temp, path)

validation = json.loads((P / 'native-traffic-validation.json').read_bytes())
assert validation['exitCode'] == 0 and not validation['timedOut'] and validation['realProfileUnchanged']
log = (P / 'native-traffic.log').read_text(encoding='utf8')
assert not any(marker in log for marker in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:'])
data = json.loads((P / 'native-traffic-evidence.json').read_bytes())
data['scope'] = (P / 'native-traffic.gd').read_text(encoding='utf8').split('"scope":"', 1)[1].split('"', 1)[0]
atomic(P / 'native-traffic-evidence.json', (json.dumps(data, indent=2) + '\n').encode())
assert data['failures'] == 0 and len(data['results']) == 8
assert all(row['introduced'] and row['detours'] == 1 and row['maxWait'] >= .25
           and not row['canceledTurns'] and not row['unfinishedTurnInterruptions']
           for row in data['results'])
turns = sum(len(row['turns']) for row in data['results'])
assert turns == 30
handoff = f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James crew-traffic turns

## Objective and acceptance
Continue James's full animation and consistency goal. This is agent-verified traffic
coverage, not full-set completion or new owner visual acceptance.

## Accepted decisions and constraints
Keep the selected masters, anatomical density, matte colour grade, equipment and clocks.
Existing reversible-work authorization applies. No runtime art/code, layout, export or
commit changed in this pass; the preceding waypoint/turn-clearance fix remains selected.

## Current state
`character/james-console-water-exit-turn-v1/build_native_traffic.py` derives
`native-traffic.gd` from the preceding next-task fixture. The native main crew update
runs flooding/vitals, safety, peer avoidance, chooser/update and passage yielding.
After normal console service/egress, normal seed17 curiosity selection gives James his
next path. A fixture recovered Bill is placed48 units ahead in a clear adjacent-room
lane, idles naturally and may yield; James's path/facing are not injected. Equal initial
water and disabled fixture pumps isolate traffic from changing flood height.

## Verification
{data['checks']:,} checks, eight journeys (four rotations, bare breathable.65 and sealed
helmet.95), eight actual detours, peak wait291.7ms in every case, {turns} ordinary turns.
All turn starts and finite completions pass, all journeys reach the next task, selected
poses fit their actual swim/tread profiles, and foot separation remains at least32 units.
Current recovered-roster rules exclude unintended Veld/Marsh spawning. Clean native log,
exit0, no timeout and real profile unchanged under scratch APPDATA. Bare/helmet waiting
native screenshots visually reviewed: bodies separated and James turns away from Bill.
These stills are not an exhaustive per-pixel overlap audit of every frame.

Investigation retained in `initial-traffic-*`, `tread-profile-diagnostic-*` and
`legacy-extra-peer-traffic-*`. First fixture wrongly treated a restart after treading
as an ordinary turn and used swim clearance for a stationary tread. Clearing architect
state enabled legacy presence and allowed Veld to respawn during full main update;
the final fixture retains current roster rules and asserts no unintended actors.
Those earlier intervals are diagnostic evidence, not the final scoped proof.

## Next action
Continue other traffic patterns, equipment transitions and complete furniture/meal and
exterior/airlock return journeys. Other seeds/layouts, high-water bare survival and
all-frame pair silhouette overlap remain distinct. Full James goal stays active.
'''
atomic(R / 'docs/JAMES_TRAFFIC_TURN_HANDOFF_2026-09-30.md', handoff.encode())
lesson = f'''\n### {TITLE}

Actual main crew update plus passage yielding now verifies eight console-to-next-task
traffic journeys: {data['checks']:,} checks, eight detours, {turns} complete ordinary turns,
zero skipped starts or unfinished turns, real profile unchanged. Native bare/helmet
waiting stills show separated bodies and turning away from the peer. This is scoped
seed17/four-rotation coverage, not every crowd pattern or full-frame overlap proof.

Use current roster presence rules for full-update fixtures. Clearing `architect_run`
activates legacy crew presence; setting an actor inactive once does not prevent its
normal respawn. Assert unintended actors stay inactive. Match body clearance to the
actual swim/tread state, and classify starts after treading as restarts rather than
ordinary direction turns. Foot separation alone is not visual overlap acceptance;
inspect native two-actor frames with both already updated and visible.

No selected pixels, source grade, size or motion clock changed. See
docs/JAMES_TRAFFIC_TURN_HANDOFF_2026-09-30.md. Full James animation goal remains active.
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

Actual main crew update and passage yielding pass {data['checks']:,} checks across eight
console-to-next-task encounters, four rotations/two gear modes: eight detours and{turns}
complete ordinary turns, no skipped starts or cut-offs. Current roster guards exclude
unintended crew. Bare/helmet waiting frames visually reviewed; foot separation and
selected swim/tread poses clear. Scratch profile, clean log, owner files unchanged.
Selected art/code unchanged this pass. Other crowd patterns and complete life/exterior
journeys remain; full goal active. [Handoff](JAMES_TRAFFIC_TURN_HANDOFF_2026-09-30.md).

'''
    atomic(status, section.encode() + before, before)
print(json.dumps({'checks': data['checks'], 'journeys': 8, 'detours': 8,
                  'ordinaryTurns': turns, 'fullSetComplete': False}))
