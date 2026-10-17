from pathlib import Path
import json, hashlib, os, uuid
P = Path(__file__).resolve().parent
R = P.parents[1]

def atomic(p, data):
    temporary = p.with_name(p.name + '.' + uuid.uuid4().hex + '.tmp')
    temporary.write_bytes(data)
    os.replace(temporary, p)

def read(p):
    return json.loads(p.read_bytes())

def write(p, value):
    atomic(p, (json.dumps(value, indent=2) + '\n').encode('utf-8'))

before = read(P / 'runtime-input-before.json')
after = {f: hashlib.sha256((R / f).read_bytes()).hexdigest() for f in before}
assert before == after, 'Frozen runtime inputs changed'
write(P / 'runtime-input-after.json', after)
guards = {}
for fixture in ['north', 'east', 'south', 'west', 'pause', 'hull_regression', 'bill_compat']:
    guard = read(P / (fixture + '-validation.json'))
    assert guard['exitCode'] == 0 and not guard['timedOut']
    assert guard['realProfileUnchanged'] and not guard['profileDelta']
    assert 'ERROR:' not in (P / (fixture + '.log')).read_text(encoding='utf-8')
    assert (P / (fixture + '.gd.uid')).exists()
    guards[fixture] = {k: guard[k] for k in ['exitCode', 'timedOut', 'realProfileUnchanged', 'profileDelta']}
assert 'WARD REPAIR: PASS' in (P / 'bill_compat.log').read_text(encoding='utf-8')
review = read(P / 'review-evidence.json')
assert review['captures'] == review['nativeRGBAMatches'] == 375
assert review['checks'] == 30759 and review['freshContinues'] == 12
for direction in ['north', 'east', 'south', 'west']:
    p = P / direction / 'native-evidence.json'
    evidence = read(p)
    assert evidence['failures'] == 0
    evidence['fixtureInheritedScope'] = evidence['scope']
    evidence['scope'] = ('Actual paid dry helmeted James ' + direction + ' cryo-ward job, genuine core release, dedicated access geometry, normal navigation/work/economy/reward. Original paired draw/held/stow sources, eighteen seconds and eight Metal, three paused real disk fresh-scene Continues. Worn gear prescribed through supported setter; not locker fitting, other ward kinds, natural owner layouts or power/door/flood interruptions.')
    write(p, evidence)
    review['cases'][direction]['scope'] = evidence['scope']
review['visualReview'] = {'nativeBoardsReviewed': 6, 'sourceBoardsReviewed': 10, 'masterReviewed': True, 'assessment': 'All375 captured sources/native views reviewed against helmeted standing masters. Stable helmet/head placement, planted physical feet, original matte grade and184 canvas/p92,172/148 standing ruler retained. West raised torch clearance retained. Dedicated fixture acceptance only; owner review pending.'}
write(P / 'review-evidence.json', review)
pause = read(P / 'north/pause-evidence.json')
pause_review = read(P / 'pause-review.json')
regression = read(P / 'hull-regression-evidence.json')
assert pause['checks'] == 340 and pause['failures'] == 0
assert pause_review['captures'] == pause_review['helmetSourceRGBAMatches'] == 27
assert regression['checks'] == 740 and regression['failures'] == 0
pause_review['visualReview'] = {'nativeBoardsReviewed': 1, 'sourceBoardsReviewed': 1, 'assessment': 'All27 North return/reentry views reviewed; original helmeted sources, stable head, matte grade and fixed physical foot retained.'}
write(P / 'pause-review.json', pause_review)
selection = {
    'status': 'installed_dry_helmet_ward_native_fixture_reviewed_owner_review_pending',
    'productionFiles': ['scripts/branforth_npc.gd', 'scripts/james_hull_resume.gd', 'scripts/james_hull_return.gd', 'scripts/bill_npc.gd'],
    'sourcesChanged': False, 'newSourceStates': 0, 'fullSetComplete': False,
    'explicitChecks': 31839, 'failures': 0, 'nativeCaptures': 402, 'sourceRGBAMatches': 402, 'freshContinues': 14,
    'lifecycleReview': 'review-evidence.json', 'pauseReview': 'pause-review.json',
    'compatibility': {'bareHull': regression, 'billWard': 'Original tests/test_ward_repair.gd passes; no invented assertion count.'},
    'guards': guards, 'frozenInputs': 'Eleven whole-file hashes equal before all seven final launches and afterward.',
    'archive': 'before-helmet-ward-admission: first North/West runs rejected helmet weld snapshots in shared validator. Archived failed logs and evidence; fixtures now fail fast. Narrow explicit James ward admission fixed production mismatch without stripping equipment or relaxing default shared validation.',
    'scope': 'Four dedicated dry helmet cryo-ward lifecycle fixtures; North actual pause/return/reentry. Prescribed worn gear, not locker fitting. Original source timing and cost retained. Source-only paid-clock GIF is not continuous native effects footage. Full set and owner acceptance remain pending.'
}
write(P / 'selection-review.json', selection)
for relative in ['character/james-ward-lifecycle-v1/selection-review.json', 'character/james-ward-cardinal-v1/selection-review.json', 'character/james-ward-clearance-v1/selection-review.json', 'character/james-torch-material-residue-v2/selection.json']:
    p = R / relative
    value = read(p)
    value['wardHelmetLifecycleReview'] = 'character/james-ward-helmet-v1/selection-review.json'
    write(p, value)
note = '''## James dry helmet ward lifecycle installed — October 1, 2026

character/james-ward-helmet-v1 extends the installed ward draw/weld/stow and
North pause/return/reentry to the original paired helmet sources. Four production
files: branforth_npc, james_hull_resume, james_hull_return and bill_npc. Canonical
saved motion recipes now bind owning family and equipment, and select matching
whole source clips. Legacy missing equipment remains bare. The two accepted
manifests have equal state IDs/counts/durations, allowing the original timing
recipe to be reused without retiming, rescaling or repainting. No new artwork.
Ward raised-tool approach clearance now covers both dry gears using previously
verified paired flame offsets. Original18seconds/8Metal and reward remain.

Shared snapshot admission initially rejected helmeted weld state; first North/
West failures are archived before-helmet-ward-admission. James explicitly opts
into dry active ward-only helmet welding admission. Shared default, helmet Hull/
construction and flooded welding remain rejected. Never strip equipment from a
save to bypass admission. Fixtures fail fast after snapshot errors.

30759 lifecycle checks0failures across four directions/375 native captures and
12 paused real disk fresh-scene Continues. North actual pause/return/reentry:
340 checks0failures/27 captures/two fresh Continues, exact held-source join,
frozen work/cost/foot during transitions, wrong equipment/family rejection and
immediate death priority. Bare Hull canonical compatibility740 checks0failures/
180 prescribed samples includes20 narrow helmet ward admission checks; this is
not new physical Hull acceptance. Original Bill ward fixture passes. Seven final
engine0/no-timeout clean logs, scratch APPDATA and strict owner profile unchanged.
Eleven whole-file inputs frozen before all final launches equal afterward.

All402 source RGBA matches verified; six lifecycle native and ten source boards,
both pause boards and four-direction helmet master comparison visually reviewed.
Original184/p92,172/148 standing ruler, matte grade, helmet/head placement and
planted feet retained; West tool clearance retained. Review pending owner
acceptance. ward-cardinal-paid-clock.gif reconstructs original sources at the
18-second paid clock, not continuous native lighting/effects gameplay footage.
Inherited bare fixture scope prose is preserved separately and corrected in
evidence metadata; counts and recorded source/physical data were not changed.

Lesson: source parity alone does not prove runtime or saved-state admission.
Bind gear and family to canonical return/reentry recipes, retain legacy defaults,
and prove actual fresh Continue with the selected gear. Review physical native
worksites and original source/master quality separately.

Remaining: helmet Hull/construction lifecycle hooks, other-facing interruptions,
locker fitting integration, electrical/other ward kinds, natural owner layouts,
power/door/critical flood/incoming workers, moving furniture/claimed-point and
full silhouette clearance; full-set/cross-family/rotation/owner/export polish.
The full James animation objective remains active and incomplete.
'''
guides = [R/'docs/CURRENT_STATUS.md', R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R/'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for index, p in enumerate(guides):
    data = p.read_bytes()
    assert note.splitlines()[0].encode() not in data
    atomic(p, note.encode() + b'\n' + data if index == 0 else data.rstrip(b'\r\n') + b'\n\n' + note.encode())
handoff = '''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James dry helmet ward lifecycle

## Objective and acceptance
Full James set matching masters, then cross-family polish. This milestone covers
four dry helmet cryo-ward jobs and North interruption, owner review pending.
The full objective remains incomplete.

## Accepted decisions and constraints
Original matte sources,184 canvas/p92,172/148 standing ruler,18seconds/8Metal.
Preserve owner profile/furniture and concurrent Bill/Veld work. Supported worn
gear setter is prescribed; locker fitting and natural owner layouts unproved.

## Current state
Four production files: branforth_npc, james_hull_resume, james_hull_return,
bill_npc. Gear-bound whole-source return/reentry; legacy bare defaults retained.
James-only dry helmet ward admission; default shared validator remains strict.
Raised-tool clearance applies both dry gears. No new art. Seven paired UID
fixtures, selection/review evidence, five guides and four parent links recorded.

## Verification
31839 explicit checks0failures; Bill ward passes separately.402 source/native
views match original paired RGBA; all native/source/master boards reviewed.
14 real disk fresh-scene Continues. Seven final engine0/no-timeout clean logs,
scratch APPDATA and strict owner profile unchanged; eleven prelaunch/after hashes
equal. Initial admission failures archived, narrow opt-in fixed; fail-fast fixture
repair. Metadata scope corrected with inherited wording preserved. GIF uses
original sources at paid clock, not continuous native gameplay footage.

## Next action
Helmet Hull/construction lifecycle and other-facing interruptions; locker fitting,
other ward/electrical/power/door/flood/incoming-worker contexts, owner layouts and
moving furniture/claimed-point/full silhouette clearance; full-set/master/
cross-family/rotation/owner/export polish. Goal remains active.
'''
atomic(P / 'HANDOFF.md', handoff.encode('utf-8'))
print(json.dumps({'explicitChecks':31839, 'captures':402, 'freshContinues':14, 'guards':7, 'frozenInputs':11, 'guidesUpdated':5}))
