"""Record complete-route evidence and its visual limits; do not admit staged art."""
from pathlib import Path
import json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'character/marsh-cargo-held-material-v1/delivery-02-actor-review'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

for name, checks, captures, samples in [
    ('cargo-delivery-01', 3298, 97, 1244),
    ('cargo-delivery-02', 3722, 117, 1244),
    ('cargo-arrival-branches-01', 1058, None, 300),
]:
    audit = ROOT / f'output/marsh-animation-audit/{name}-2026-10-02'
    report = read(audit / 'report.json')
    assert (report['checks'], report['failures'], len(report['samples'])) == (checks, 0, samples)
    assert (audit / 'native-exit.txt').read_text().strip() == '0'
    assert 'ERROR:' not in (audit / 'native.log').read_text()
    for kind, count in [('inputs', 615), ('owner', 2931)]:
        before = read(audit / f'{kind}-before.json')
        assert len(before) == count and before == read(audit / f'{kind}-after.json')
    if captures is not None:
        assert len(report['captures']) == captures
        assert sum(case['actorRestores'] for case in report['cases']) == captures
        assert all(case['completed'] and case['samples'] == 311 for case in report['cases'])
    else:
        assert [(c['incoming'], len(c['turnSlots']), c['actorRestores']) for c in report['cases']] == [
            ('east', 5, 9), ('south', 9, 13), ('north', 0, 4)]

assessment = {
    'normalAdmission': False, 'fullGoalComplete': False,
    'allPairsInspected': True, 'pairedBoardsInspected': 16, 'sourceNativePairsInspected': 117,
    'findings': 'All complete-route pairs inspected. Source/native correspondence holds. '
        'West-to-North arrival now uses all five authored poses before lowering instead of '
        'an instantaneous yaw. Exact turn endpoint/unload opening matches. Stationary arrival '
        'uses walking leg poses; pivot contact remains provisional. Side intermediate body '
        'breadth, head proportions, colour grade, rigid-case consistency and floor contact '
        'remain polish findings; this review does not accept the full master-matched set.',
    'limits': 'Controlled furnished-fixture normal controller routes with privately staged '
        'sources. Actor/player snapshots are not full RunSave or fresh visible Title Continue. '
        'Not continuous contact film, helmet acceptance, paid expedition or normal art admission.'
}
(REVIEW / 'visual-assessment.json').write_text(json.dumps(assessment, indent=2) + '\n', encoding='utf-8')
subprocess.run([sys.executable, str(ROOT / 'tools/publish_marsh_cargo_delivery02.py')], check=True, stdout=subprocess.DEVNULL)
verification = read(REVIEW / 'verification.json')
assert verification['visualReviewed'] and len(verification['boards']) == 16

maintained = ROOT / 'skills/brinespace-character-pipeline/references/master-repair.md'
installed = Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert maintained.read_bytes() == installed.read_bytes()
marker = '## Marsh complete cargo routes and arrival presentation — October 2, 2026'
lesson = '''

## Marsh complete cargo routes and arrival presentation — October 2, 2026

Full master-matched Marsh animation set and all-family consistency/polish remain
active and incomplete. Preferred private cargo family is SouthNorth01/EastWest02;
normal catalogue selections remain unchanged. See MARSH_CARGO_DELIVERY02_HANDOFF.

Complete normal controller deliveries starting East/West/South/North with the
preferred staged carry/turn/held family exposed a missing join: every automatically
planned route ended carrying West, while inherited arrival immediately faced North
for unloading. Isolated clip tests and exact endpoints did not catch that yaw jump.
Baseline delivery01: 3298 checks, 97 captures, 1244 controlled 20ms samples, 97
actor/player restores; baseline boards were not all visually reviewed. Preserve
that evidence as the before-change scope, not current runtime acceptance.

Marsh-only workshop_arrival_origin records incoming East/West/South. Presentation
plays the authored carry turn, then unload-north, within the existing two-second
arrival timer. Routes, North arrival facing and gameplay duration are unchanged.
North arrival needs no turn; absent turn clips preserve legacy presentation. Actor
snapshot persists origin, validates its context and defaults missing old-save
fields to empty. Grid uses this derived presentation clock before generic unload.
No raster changed; Bill's inherited behavior remains untouched.

Fresh delivery02: 3722 checks, four completed normal routes, 117 exact-source/native
pairs, 1244 controlled samples (311 each), 117 actor/player restores plus pause.
All five West-to-North arrival poses precede four unload poses. All 117 pairs across
16 boards inspected. Seeded actual arrive/update East/South/North branches: 1058
checks, 300 samples, 26 restores; 5/9/0 turn slots respectively plus four unload
slots, old-field compatibility and malformed/context rejection. Seeded branches
are not three additional complete routes or visually accepted pivots.

Each of the three audit intervals independently held 615 bounded inputs stable
and 2931 owner non-log files unchanged under scratch APPDATA, zero failures/errors,
exit zero. These are dated interval freezes, not equality across the runtime edit
or later metadata updates. Source/native parity and coherent sequencing pass;
body/head breadth, grade, rigid case and sole/floor contact remain provisional.
Stationary arrival reuses walking-leg turn poses: inspect/author physical pivot
contact before claiming smooth grounded motion. Mechanical success is not artwork
acceptance. Full RunSave plus fresh visible Title Continue, helmet context and
normal coherent-family admission remain pending; remaining full-set families and
cross-family polish remain required. No live native job at this milestone.
'''
for path in [ROOT / 'character/ANIMATION_PIPELINE.md', ROOT / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', ROOT / 'docs/CURRENT_STATUS.md', maintained]:
    with path.open(encoding='utf-8') as handle:
        present = any(marker in line for line in handle)
    if not present:
        with path.open('a', encoding='utf-8') as handle:
            handle.write(lesson)
installed.write_bytes(maintained.read_bytes())

(ROOT / 'docs/MARSH_CARGO_DELIVERY02_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh complete cargo routes and arrival

## Objective and acceptance
Complete the full master-matched Marsh animation set and all-family consistency/
polish. Active/incomplete. Cargo sequencing milestone, not full art acceptance.

## Accepted decisions and constraints
Preferred staged family SouthNorth01/EastWest02; normal catalogue unchanged.
Whole figures, own-facing identity, exact endpoints and one neutral scale.
Preserve normal routes, North arrival facing and two-second timer. Scratch APPDATA
and owner fingerprints required. Preserve unrelated/concurrent large script edits.

## Current state
scripts/marsh_npc.gd adds incoming cargo arrival presentation and validated snapshot
field; scripts/grid_canvas.gd renders its turn/unload clock. No raster changes.
Delivery01/02 and arrival-branches01 fixture .gd/.uid pairs and prepare/fingerprint
helpers added, both delivery publishers and delivery02 recorder added.
character/marsh-cargo-held-material-v1/delivery-02-actor-review contains 117 pairs,
16 reviewed boards and scoped assessment. Pipeline/bible/status/skill mirrors updated.

## Verification
Baseline 3298 checks/97 captures identified abrupt West->North arrival. After fix:
3722 checks, 4 completed normal controller routes, 1244 samples, 117 restores+pause,
117 exact source/native pairs visually inspected. All five arrival-turn poses then
four unload poses. Additional seeded East/South/North actual-arrive branches:
1058 checks, 300 samples, 26 restores, compatibility/context validation. All audits
615 bounded inputs stable per interval, 2931 owner files unchanged, 0 errors/failures,
exit 0. No live job. Baseline boards not all reviewed; seeded branches no visual claim.

## Next action
Independent full RunSave and fresh visible Title Continue gates. Review grounded
arrival pivot (current stationary turn uses walking legs), remaining proportions/
grade/case/contact and helmet context before normal coherent-family admission.
Continue remaining Marsh families and full cross-family consistency/polish.
''', encoding='utf-8')
print('Recorded: 3722 route checks / 1058 branch checks; 117 visual pairs; goal incomplete.')
