from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
ROOT = P.parents[1]
dest = P / 'lowered-entry-evidence.json'
assert not dest.exists(), 'Milestone already recorded; preserve its evidence.'
cases = [
    ('bill-death-ground-lowered-mortality-candidate-native-v1', 539),
    ('bill-death-ground-station-candidate-v1', 133),
    ('bill-ground-death-snapshot-v1', 17),
    ('bill-death-ground-mortality-candidate-native-v1', 459),
]
reports = {}
paths = []
for folder, count in cases:
    out = ROOT / 'output' / folder
    report = json.loads((out / 'validation.json').read_text())
    log = (out / 'native.log').read_text()
    assert report['returnCode'] == 0
    assert f'{count} checks,0 failures' in log
    reports[folder] = dict(checks=count, **report)
    paths.extend(out / name for name in ['validation.json', 'native.log', 'profile-before.json', 'profile-after.json'])
review = json.loads((P / 'station-review.json').read_text())
assert review['status'] == 'lowered_entry_reviewed_counter_overlap_pending'
assert len(review['sha256']) == 48
summary = '''Bill lowered dry-collapse entry — October 1, 2026.
Bill/Major Bill candidate family opts into a saved initial fall phase. Kneel,
repair and stand callers skip the upright prefix when lowered. Other actors and
normal art selection remain unchanged. Existing cosmetic death clock is retained.
East/west choose an authored pose using crown extent; axial falls use authored
kneeling slot 2 (.55s), since projected crown height is not a posture invariant.
Snapshots accept only six authored prefixes; legacy absent fields restore to zero.
539 lowered mortality/restore checks, 133 station-render checks, 17 snapshot checks
and 459 upright mortality regression checks pass. Each overall runner remains
FAILED: last_session.json changed among 2,928 real non-log files. Explicit scratch
profiles and deltas retained; live project activity observed, no owner restoration
or retrospective clean-profile claim. Earlier failed axial crown assertions remain
archived; their measurement was too restrictive for forward/backward projection.
48 current station captures hash-bound; counter and aisle boards visually reviewed.
Standing reset addressed, but exact limb/torso joins still differ: some equipped
side entries skip farther into the fall. North terminal still overlaps the counter.
No claim of anatomical continuity or full furniture clearance. Sitting, bunk, cargo
and arbitrary tool joins, normal binding and fresh title-screen Continue remain.
Generic rest, meal/inspection proof and full-set master consistency/polish remain.
No owner layout, route, reward, economy, commit or export changes. Goal stays active.
'''
heading = '## Bill lowered dry-collapse entry — October 1, 2026\n\n'
old = (P / 'HANDOFF.md').read_text(encoding='utf-8')
handoff = '''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill animation continuation

## Objective and acceptance
Complete the master-consistent Bill library, including visible actual-room joins.

## Accepted decisions and constraints
Keep matte identity, authored anatomy, owner room geometry and scratch-only tests.
Candidate review is not owner acceptance or normal runtime selection.

## Current state
New scripts/bill_ground_death.gd; narrow Bill snapshot, player metadata and renderer
hooks; family deathEntryMode opt-in. New lowered mortality/station/schema fixtures,
runners and review evidence. No source pixels changed at this milestone.

## Verification
'''+summary+'''
## Next action
Resolve north counter occlusion/physical clearance and finer lowered joins before
normal art binding. Preserve prior evidence and concurrent crew work.

## Earlier evidence

'''+old
(P / 'HANDOFF.md').write_text(handoff, encoding='utf-8')
for rel in ['scripts/bill_ground_death.gd', 'scripts/bill_npc.gd', 'scripts/crew_sprite_player.gd', 'scripts/grid_canvas.gd', 'tests/test_bill_death_ground_station_lowered_candidates.gd', 'tests/test_bill_death_ground_lowered_mortality_candidates.gd', 'tests/test_bill_ground_death_snapshot.gd']:
    f = ROOT / rel
    paths.extend([f, f.with_suffix(f.suffix + '.uid')])
paths.extend(P / name for name in ['build.py', 'manifest.json', 'helmet-manifest.json', 'HANDOFF.md', 'station-review.json', 'station-review.html', 'station-counter-review.png', 'station-aisle-review.png', 'prepare_lowered_validation.py', 'prepare_snapshot_validation.py', 'record_lowered_entry.py'])
paths.extend(ROOT / 'tools' / name for name in ['run_bill_death_ground_station_lowered_candidate_validation.py', 'run_bill_death_ground_lowered_mortality_candidate_validation.py', 'run_bill_ground_death_snapshot_validation.py'])
dest.write_text(json.dumps(dict(status='staged_lowered_entry_counter_overlap_pending', reports=reports, captureBindings=review['sha256'], scope=summary, sha256={f.relative_to(ROOT).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}), indent=2)+'\n', encoding='utf-8')
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md', 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', 'skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT / rel).open('a', encoding='utf-8') as f:
        f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a', encoding='utf-8') as f:
    f.write('\n'+heading+summary)
f = ROOT / 'docs/CURRENT_STATUS.md'
f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-family-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded lowered-entry milestone; 1,148 subsystem checks pass, four overall profile guards fail; visual joins remain open.')
