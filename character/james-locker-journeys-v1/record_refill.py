from pathlib import Path
import json
import uuid
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parents[1]
TITLE = 'James actual locker refill and reservation — September 30, 2026'

def atomic(path, data, before=None):
    if before is None:
        before = path.read_bytes() if path.exists() else None
    temporary = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    temporary.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None) == before
    temporary.replace(path)

evidence = json.loads((P / 'native-locker-refill-evidence.json').read_bytes())
assert evidence['failures'] == 0 and len(evidence['results']) == 4
for name in ['native-locker-refill', 'test_station_systems']:
    report = json.loads((P / (name + '-validation.json')).read_bytes())
    assert report['exitCode'] == 0 and not report['timedOut'] and report['realProfileUnchanged']
    log = (P / (name + '.log')).read_text(errors='replace')
    assert not any(marker in log for marker in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:'])

board = Image.new('RGB', (864, 912), (45, 58, 63))
for q in range(4):
    image = Image.open(P / 'refill-captures' / f'q{q}-refill-held.png').convert('RGB')
    assert image.size == (432, 432)
    x, y = q % 2 * 432, q // 2 * 456
    board.paste(image, (x, y + 24))
    ImageDraw.Draw(board).text((x + 5, y + 5), f'Actual refill / airlock rotation {q}', fill='white')
board.save(P / 'native-refill-contact.png')

handoff = f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James refill journey

## Objective and acceptance
Continue full animation/style consistency. Actual station refill joins reviewed by
agent; no new source art or owner acceptance claimed. Full James goal stays active.

## Accepted decisions and constraints
Refill remains the existing five-second fitted idle hold and normal12 units/s oxygen
service. Selected matte idle cycle, perspective, registration and gear unchanged.
No room layouts, owner profile, export or commit changed.

## Current state
Four actual airlock routes found the reservation ended when the approach request
cleared. AirlockService now recognizes the saved refill hold and reserves it for
other actors, rejects repeat/helmet-change requests and ends it on service loss.
Airlock panel reflects active hold; existing full-tank expedition dispatch remains
available and releases the reservation. Changes: scripts/airlock_service.gd,
scripts/airlock_panel.gd. Derived fixture/builder and review under
character/james-locker-journeys-v1; productionFittingRefill metadata updated.

## Verification
{evidence['checks']:,} native checks, four rotated equipped refill routes, four actual disk
Continue restores. Actual vitals reach full tank; finite hold, contact, selected
equipped idle-cycle pixels, unchanged gear, paused clock and exact saved actor pass.
Reservations survive Continue; duplicates refused, completion releases, power loss
ends hold and grants no oxygen. Existing full-tank dispatch behavior retained.
Station systems regression passes. Serial scratch native runs clean/exit0/no timeout;
real owner profile unchanged. Four native full-locker captures visually reviewed.
Prior diagnostic confirmed four missing reservations. Its frame-zero equality failures
were a fixture error: idle is animated. Current assertion checks selected cycle membership.

## Next action
Actual second-crew locker crowd/body journey, then furniture/meals and full exterior
return joins. Refill currently uses idle; no hose/valve animation has been authored.
Other layouts, bare refill requests and emergency/layout interruption journeys remain
separate. Full animation coverage and final cross-family polish still unproven.
'''
atomic(R / 'docs/JAMES_REFILL_JOURNEY_HANDOFF_2026-09-30.md', handoff.encode())
path = R / 'character/james-helmet-fitting-east-v1/selection.json'
before = path.read_bytes()
selection = json.loads(before)
selection['productionFittingRefill'] = {'checks': evidence['checks'], 'journeys': 4, 'actualRestores': 4, 'evidence': 'character/james-locker-journeys-v1/native-locker-refill-evidence.json', 'art': 'Existing selected equipped idle cycle; no new refill art.', 'fullSetComplete': False}
selection['limitations'] = ['Standard fitting/reversal/Continue and four equipped refill routes verified. Actual second-crew crowd body journeys, other layouts, bare refill requests, hose/valve source motion and emergency interruptions remain separate.']
selection['next'] = 'Continue actual second-crew locker journey, furniture/meals and full exterior return; full James goal active.'
atomic(path, (json.dumps(selection, indent=2) + '\n').encode(), before)
lesson = f'''\n### {TITLE}

Approach reservations must survive a subsequent service hold even when the pending
request clears. Derive existing refill intent from saved idle/activity/timer/path,
reserve until completion, reject duplicate requests and preserve it through Continue.
Do not assert an animated idle equals frame zero; compare selected cycle membership.
{evidence['checks']:,} native checks/four actual rotated equipped refills/four disk restores
pass. Power loss ends hold with no credit; full-tank dispatch remains available. Selected
matte idle cycle unchanged and full locker captures reviewed. No new hose/valve source
art or actual second-crew body journey claimed. Full James goal active; see
docs/JAMES_REFILL_JOURNEY_HANDOFF_2026-09-30.md.
'''
for path in [R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R / 'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before = path.read_bytes()
    if TITLE.encode() not in before:
        atomic(path, before + lesson.encode(), before)
path = R / 'docs/CURRENT_STATUS.md'
before = path.read_bytes()
if TITLE.encode() not in before:
    section = f'''## {TITLE}

Four actual rotated equipped refills/four Continue restores pass{evidence['checks']:,} checks.
Fixed reservation loss during the existing five-second idle hold; duplicate requests
refused, completion releases, power loss ends/no credit. Dispatch timing retained. Selected
matte idle art unchanged; four full-locker native views reviewed. Station systems
regression clean; scratch runs preserve owner profile. Actual second-crew body journey,
new hose/valve motion, other layouts and full consistency polish remain. Goal active.
[Handoff](JAMES_REFILL_JOURNEY_HANDOFF_2026-09-30.md).

'''
    atomic(path, section.encode() + before, before)
print(f'Recorded {evidence["checks"]} refill checks and native contact board; full goal active')
