from pathlib import Path
import json
import uuid
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parents[1]
TITLE = 'James two-crew locker handoff — September 30, 2026'

def atomic(path, data, before=None):
    if before is None:
        before = path.read_bytes() if path.exists() else None
    temporary = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    temporary.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None) == before
    temporary.replace(path)

evidence = json.loads((P / 'native-locker-crowd-evidence.json').read_bytes())
assert evidence['failures'] == 0 and len(evidence['results']) == 12
for name in ['native-locker-crowd', 'test_station_systems', 'test_parts_passage', 'test_branforth_crew']:
    report = json.loads((P / (name + '-validation.json')).read_bytes())
    assert report['exitCode'] == 0 and not report['timedOut'] and report['realProfileUnchanged']
    log = (P / (name + '.log')).read_text(errors='replace')
    assert not any(marker in log for marker in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:'])

board = Image.new('RGB', (864, 912), (45, 58, 63))
for q in range(4):
    image = Image.open(P / 'crowd-captures' / f'q{q}-equip-helmet-next-crew.png').convert('RGB')
    assert image.size == (432, 432)
    x, y = q % 2 * 432, q // 2 * 456
    board.paste(image, (x, y + 24))
    ImageDraw.Draw(board).text((x + 5, y + 5), f'Actual second-crew fitting / rotation {q}', fill='white')
board.save(P / 'native-crowd-contact.png')
minimum = min(row['minimumSeparation'] for row in evidence['results'])
maximum_wait = max(row['peakWait'] for row in evidence['results'])
handoff = f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James locker crowd handoff

## Objective and acceptance
Continue full James animation/style and journey consistency. Native handoffs agent
reviewed; no new source art, new owner acceptance or full-set completion claimed.

## Accepted decisions and constraints
Selected James matte sources, master scale, poses, clocks and gear commits unchanged.
Other actor artwork and owner layouts preserved. Native tests use scratch profiles.

## Current state
Actual second-crew locker approach could deadlock and lose its explicit request.
Shared CrewPassage now permits normal retreat-and-return on pending approaches,
while active fitting and refill contacts remain stationary. Bill movement preserves
explicit locker intent through temporary crew waits; service/geometry cancellation
still applies. Traffic replanning preserves James's authored East connector instead
of generic smoothing away the final facing. Shared files: scripts/crew_passage.gd,
scripts/bill_npc.gd.
Builder/fixture, baseline and focused traces, native views under
character/james-locker-journeys-v1. Selection, pipeline/bible and skill mirrors updated.

## Verification
{evidence['checks']:,} native checks,12 actual two-crew journeys: four airlock rotations
times James fitting, removal and equipped refill. Fixture recovered Bill starts at
a clear nearby airlock point. Real second service requests refuse while occupied,
accept after release; normal native crew/passages and James next-task chooser run.
Both traveled legs clear; minimum foot separation{minimum:.3f}; maximum measured
wait{maximum_wait:.3f}s. James arrives East without fitting snap, held pixels/clock/
fixed contact/gear retained, next walk uses committed gear. Bill completes fitting.
24 native service/handoff views reviewed. Station systems, parts passage and James
crew regressions pass. All serial/scratch runs clean/exit0/no timeout; owner unchanged.
Baseline285,985 checks/12 failures and focused snapshots retain the original request
loss/deadlock evidence. No disk Continue in crowd fixture; individual fitting/refill
Continue evidence remains separate. Foot separation is not all-frame alpha-overlap QA.

## Next action
Continue furniture/meal acquisition, contact and departure joins, then full exterior
sample/cargo/airlock-return journey. Other traffic placements, customized furniture,
crowd checkpoint restoration, refill hose/valve art and final cross-family polish
remain. Full James goal stays active; no export or commit.
'''
atomic(R / 'docs/JAMES_LOCKER_CROWD_HANDOFF_2026-09-30.md', handoff.encode())
path = R / 'character/james-helmet-fitting-east-v1/selection.json'
before = path.read_bytes()
selection = json.loads(before)
selection['productionFittingCrowd'] = {'checks': evidence['checks'], 'twoCrewJourneys': 12, 'evidence': 'character/james-locker-journeys-v1/native-locker-crowd-evidence.json', 'minimumFootSeparation': minimum, 'review': 'Agent reviewed occupied and next-crew native views; no new owner acceptance.', 'fullSetComplete': False}
selection['limitations'] = ['Standard fitting/reversal/Continue/refill plus12 sampled two-crew handoffs verified. Other crowd placements, crowd disk Continue, customized layouts, bare refill requests, hose/valve source motion and emergency journeys remain separate.']
selection['next'] = 'Continue furniture/meal and full exterior-return joins; full James goal active.'
atomic(path, (json.dumps(selection, indent=2) + '\n').encode(), before)
lesson = f'''\n### {TITLE}

Distinguish a pending locker approach from the stationary fitting/refill action.
Approaches can use normal retreat-and-return without losing their final contact;
preserve the authored final-facing connector when rebuilding a traffic detour.
held fitting and refill cannot be nudged. Keep explicit service intent through
temporary crew waits instead of applying an ambient-goal timeout. Actual two-crew
handoffs, not reservation queries alone, exposed the request loss/deadlock.
{evidence['checks']:,} native checks/12 journeys pass, preserving East arrival, selected
James source pixels/clocks/gear and normal next walk. Native occupied/handoff views
reviewed; sources and grade unchanged. Foot separation is distinct from alpha-overlap
QA; crowd Continue/custom layouts remain open. Full James goal active; see
docs/JAMES_LOCKER_CROWD_HANDOFF_2026-09-30.md.
'''
for path in [R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R / 'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before = path.read_bytes()
    if TITLE.encode() not in before:
        atomic(path, before + lesson.encode(), before)
path = R / 'docs/CURRENT_STATUS.md'
before = path.read_bytes()
if TITLE.encode() not in before:
    section = f'''## {TITLE}

Fixed actual pending-locker deadlock/request loss using normal retreat-and-return
and retained explicit intent; fitting/refill remain stationary.12 two-crew journeys
pass{evidence['checks']:,} checks across four rotations and fitting/removal/refill. James
East arrival, selected pixels/clocks/gear and next walk retained; Bill completes next
fitting.24 native views reviewed; shared station/passage/crew regressions pass. Scratch
runs preserve owner profile. Source art unchanged; other traffic/crowd Continue,
furniture/meals/exterior and full cross-family polish remain. Full goal active.
[Handoff](JAMES_LOCKER_CROWD_HANDOFF_2026-09-30.md).

'''
    atomic(path, section.encode() + before, before)
print(f'Recorded {evidence["checks"]} two-crew checks; full James goal active')
