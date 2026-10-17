from pathlib import Path
import json
import uuid
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parents[1]
TITLE = 'James galley arrival and fresh-scene Continue — September 30, 2026'

def atomic(path, data, before=None):
    if before is None:
        before = path.read_bytes() if path.exists() else None
    temporary = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    temporary.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None) == before
    temporary.replace(path)

evidence = json.loads((P / 'native-meal-evidence.json').read_bytes())
assert evidence['failures'] == 0 and len(evidence['results']) == 8
assert all(row['arrivalHeading'] == row['facing'] and row['restorePixelsExact'] for row in evidence['results'])
for name in ['native-meal', 'test_branforth_crew']:
    report = json.loads((P / (name + '-validation.json')).read_bytes())
    assert report['exitCode'] == 0 and not report['timedOut'] and report['realProfileUnchanged']
    log = (P / (name + '.log')).read_text(errors='replace')
    assert not any(marker in log for marker in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:'])

board = Image.new('RGB', (1296, 1824), (45, 58, 63))
for q in range(4):
    paths = [P / 'captures' / f'q{q}-bare-life_eat-03-held.png', P / 'captures' / f'q{q}-bare-life_drink-03-held.png']
    row = next(row for row in evidence['results'] if row['rotation'] == q and row['mode'] == 'helmet')
    paths.append(R / row['captures'][0].removeprefix('res://'))
    for column, path in enumerate(paths):
        image = Image.open(path).convert('RGB')
        assert image.size == (432, 432)
        x, y = column * 432, q * 456
        board.paste(image, (x, y + 24))
        ImageDraw.Draw(board).text((x + 5, y + 5), f'q{q} / ' + ['eat', 'drink', 'sealed inspection'][column], fill='white')
board.save(P / 'native-galley-contact.png')
facings = sorted(set(row['facing'] for row in evidence['results']))
handoff = f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James actual galley joins

## Objective and acceptance
Continue full James animation/master consistency and journey polish. Selected meal
source art remains owner-review pending. Native galley samples agent reviewed.

## Accepted decisions and constraints
Selected matte source poses, master148 density, bare eat/drink loops, closed-helmet
inspection substitute and6+3s service budgets unchanged. Hunger excludes equipped
crew; equipped fixture uses the actual curiosity chooser. No eating through glass.

## Current state
James now plans the galley station's facing before arriving, eliminating an East-to-
South snap at the start of meals. Only scripts/branforth_npc.gd runtime hook changed.
Builder: character/james-locker-journeys-v1/build_meal_fixture.py. Native fixture,
fresh-scene restore evidence and native galley review: character/james-meal-journeys-v1.
Meal selection metadata, pipeline/bible and crew skill mirrors updated.

## Verification
{evidence['checks']:,} native checks/eight actual galley service journeys: four rotated
default galleys, bare hunger meals and equipped curiosity inspection. Normal chooser
seeds1/4, actual main crew update, real service-floor contact, held source membership,
fixed contact/gear, correct arrival facing and normal next walking join asserted.
Eight actual disk Continue restores into newly instantiated scenes preserve complete
actor state, clock, selected pixels and paused pixels. Existing playback snapshots
already preserve cosmetic phase; no new animation clock was necessary.
James crew regression passes; serial scratch runs clean/exit0/no timeout and real
profile unchanged. Native meal/drink/inspection poses, matte finish and scale reviewed.
Actual facing coverage:{','.join(facings)}. Four room rotations do not prove four facings.
An initial fixture used the wrong entrance in rotated rooms; its failures are not a
game regression. A tiny same-contact repeat meal is not a walking departure; wait
for observable walk state instead of assuming every foot correction is a walk frame.

## Next action
Resolve actual hand/counter reach, then author food/cup acquisition, dish deposit and meal interruption/
exit choreography. Current loops still introduce/replace hand props without those
explicit transitions. Review other facing contacts/custom layouts and meal credit
through interruption; full exterior cargo/airlock return and cross-family polish remain.
Full James goal active; no export, commit or full-set acceptance.
'''
atomic(R / 'docs/JAMES_GALLEY_JOURNEY_HANDOFF_2026-09-30.md', handoff.encode())
path = R / 'character/james-meal-family-v1/selection.json'
before = path.read_bytes()
selection = json.loads(before)
selection['productionGalleyJourneys'] = {'checks': evidence['checks'], 'actualJourneys': 8, 'freshSceneDiskRestores': 8, 'actualFacings': facings, 'evidence': 'character/james-meal-journeys-v1/native-meal-evidence.json', 'review': 'Agent reviewed actual counter contact, selected matte scale/poses; owner review remains pending.', 'fullSetComplete': False}
selection['remaining'] = ['Owner visual review', 'Food/cup acquisition, dish deposit, meal-to-drink/idle choreography and interruption credit', 'Other facing/custom galley contacts, complete exterior journeys and full cross-family consistency/polish']
atomic(path, (json.dumps(selection, indent=2) + '\n').encode(), before)
lesson = f'''\n### {TITLE}

Plan real counter facing before arrival instead of rotating into a meal pose at the
last waypoint. {evidence['checks']:,} native checks/eight actual default galley services
pass; actual facing here is{','.join(facings)}, despite four room rotations. Bare hunger
and equipped curiosity/inspection are different activities. Preserve closed-visor rules.
Fresh-scene disk Continue already restores saved playback phase: prove actual pixels
before inventing a new clock. Wait for observable walking departure; a tiny return to
the same contact may begin another meal. Meal loops/technical restores do not establish
pickup, deposit or smooth interruption art. Those source transitions remain open.
Service-floor contact does not prove hand/counter reach for pickup/deposit.
Selected matte sources/density unchanged; native counter samples reviewed. Full James
goal active; see docs/JAMES_GALLEY_JOURNEY_HANDOFF_2026-09-30.md.
'''
for path in [R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R / 'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before = path.read_bytes()
    if TITLE.encode() not in before:
        atomic(path, before + lesson.encode(), before)
path = R / 'docs/CURRENT_STATUS.md'
before = path.read_bytes()
if TITLE.encode() not in before:
    section = f'''## {TITLE}

Fixed counter arrival facing snap. Eight actual galley services/fresh-scene disk
Continue restores pass{evidence['checks']:,} checks: bare hunger eat/drink and sealed
curiosity inspection, native counter contact, saved pose/clock/pause and next walk.
Actual facing is{','.join(facings)} across four default room rotations. Selected matte
source/size/budgets unchanged; native samples reviewed and James crew regression passes.
Scratch profiles preserve owner files. Pickup/deposit/interrupt source joins and meal
credit checks remain, alongside other contacts/exterior/full consistency work. Goal active.
[Handoff](JAMES_GALLEY_JOURNEY_HANDOFF_2026-09-30.md).

'''
    atomic(path, section.encode() + before, before)
print(f'Recorded {evidence["checks"]} galley checks; full James goal active')
