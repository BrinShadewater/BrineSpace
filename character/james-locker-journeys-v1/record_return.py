from pathlib import Path
import json
import uuid

R = Path(__file__).resolve().parents[2]
P = Path(__file__).resolve().parent
TITLE = 'James interrupted helmet handoff returns through authored poses — September 30, 2026'

def atomic(path, data, before=None):
    if before is None:
        before = path.read_bytes() if path.exists() else None
    temporary = path.with_name(path.name + '.james-' + uuid.uuid4().hex + '.tmp')
    temporary.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None) == before, path
    temporary.replace(path)

for name in ['native-locker-return', 'native-locker-restore']:
    report = json.loads((P / (name + '-validation.json')).read_bytes())
    evidence = json.loads((P / (name + '-evidence.json')).read_bytes())
    assert report['exitCode'] == 0 and not report['timedOut'] and report['realProfileUnchanged']
    assert evidence['failures'] == 0 and len(evidence['results']) == 8
    log = (P / (name + '.log')).read_text(errors='replace')
    assert not any(marker in log for marker in ['SCRIPT ERROR:', 'ERROR:', 'WARNING:'])

path = R / 'character/james-helmet-fitting-east-v1/selection.json'
before = path.read_bytes()
selection = json.loads(before)
selection['productionFittingGuards']['abortVisualPolicy'] = 'Service loss reverses the exact held source pose to original unchanged-gear idle; other safety cancellation remains immediate.'
selection['productionFittingGuards']['powerEvidenceRevision'] = 'The 50,672-check immediate-cancel report is historical, superseded for visual policy by productionFittingReturn.'
selection['productionFittingReturn'] = {
    'checks': 54925, 'serviceLosses': 8, 'actualMidReturnRestores': 8,
    'evidence': 'character/james-locker-journeys-v1/native-locker-return-evidence.json',
    'review': 'Agent reviewed 18 native sampled reverse poses; owner fitting-art acceptance retained, new reversal awaits owner visual review.',
    'fullSetComplete': False,
}
selection['limitations'] = ['Standard four rotations: sampled service-loss reversals, eight midpoint Continue restores, retry and next-task journeys verified. Other layouts, crowded lockers, refill and emergency interruption journeys remain separate.']
selection['next'] = 'Continue furniture, meal, refill and exterior journey polish; full James goal active.'
atomic(path, (json.dumps(selection, indent=2) + '\n').encode(), before)

handoff = '''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James interrupted fitting return

## Objective and acceptance
Continue James animation consistency and complete journeys. Earlier owner fitting-art
acceptance retained. New interrupted-return motion is agent reviewed, pending owner review.

## Accepted decisions and constraints
Existing selected 12 poses, matte grade, density, endpoints and normal 2.14/2.24s clocks
unchanged. Original gear remains uncommitted through return. No new raster art or layout.

## Current state
James reverses the exact held fitting/removal pose when locker service disappears.
Shared Bill supplies default immediate interruption hooks; AirlockService invokes the
hook and preserves an active return. James owns reverse clock and validated snapshot
flag. Generic safety cancel clears reverse mode immediately. Changed runtime files:
scripts/bill_npc.gd, scripts/branforth_npc.gd, scripts/airlock_service.gd.
Builders, fixtures and native reviews: character/james-locker-journeys-v1.
Selection metadata and pipeline/bible/crew skill mirrors updated.

## Verification
54,925 checks, eight actual service losses across four rotations and two actions.
Exact initial held pixels, decreasing simulation clock, source poses, fixed foot,
uncommitted gear and reverse shelf markers. Eight actual midpoint disk Continue
restores preserve actor/timer/pixels/shelf/pause. Power returning cannot restart
unfinished motion. Every normal retry completes all12 slots and reaches next task.
Fresh normal fitting Continue regression:44,341 checks/eight restores. Station systems
regression passes. Serial scratch runs, clean logs, exit0, no timeout, real profile unchanged.
18 native reverse poses reviewed; GIF preserves sampled times with600ms endpoint holds.
Fire/flood/rebuild immediate-cancel call sites inspected; emergency journeys not replayed.
The prior50,672-check immediate-cancel evidence is historical, not current-policy proof.

## Next action
Owner review of native-return-review.gif. Continue crowded/refill locker and furniture/
meal journeys, then full exterior/airlock-return and remaining cross-family polish.
Full James goal remains active; no export, commit or full-set acceptance.
'''
atomic(R / 'docs/JAMES_FITTING_RETURN_HANDOFF_2026-09-30.md', handoff.encode())
lesson = f'''\n### {TITLE}

Locker service loss now reverses the existing selected pose using the simulation clock;
gear stays unchanged and shelf markers follow reverse elapsed time. Keep service loss
separate from immediate emergency cancellation. Snapshot reverse mode explicitly,
validate its duration/state, and restore it after rebuild clears transient actions.
54,925 native checks cover eight reversals and eight midpoint disk restores; fresh
normal Continue44,341 checks pass. Reviewed18 native poses; owner review pending.
Earlier immediate-cancel power evidence is historical. Emergency call sites inspected,
not journey-replayed. Crowds/refill/other layouts remain open; full James goal active.
See docs/JAMES_FITTING_RETURN_HANDOFF_2026-09-30.md.
'''
for path in [R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R / 'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before = path.read_bytes()
    if TITLE.encode() not in before:
        atomic(path, before + lesson.encode(), before)
path = R / 'docs/CURRENT_STATUS.md'
before = path.read_bytes()
if TITLE.encode() not in before:
    section = f'''## {TITLE}

Service loss returns the exact held fitting pose through existing art with unchanged
gear and reverse shelf markers.54,925 checks/eight reversals/eight midpoint Continue
restores pass, including pause, restored power, normal retry and next task. Fresh
normal Continue44,341 checks and station systems regression pass; owner profile unchanged.
18 native poses reviewed; new reversal awaits owner review. Emergency cancel call sites
inspected, journeys not replayed. Prior immediate-cancel evidence is historical.
Crowds/refill/furniture/meals/exterior and full consistency polish remain; goal active.
[Handoff](JAMES_FITTING_RETURN_HANDOFF_2026-09-30.md).

'''
    atomic(path, section.encode() + before, before)
print('Recorded interrupted-return milestone and superseded visual policy; full goal active')
