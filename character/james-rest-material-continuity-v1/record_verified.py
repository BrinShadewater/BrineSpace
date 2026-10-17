from pathlib import Path
import json, os, uuid

P = Path(__file__).resolve().parent
R = P.parents[1]
n = json.loads((P / 'validate-evidence.json').read_text())
w = json.loads((P / 'validate-validation.json').read_text())
v = json.loads((P / 'packaging-validation.json').read_text())
assert n['failures'] == 0 and len(n['journeys']) == 2
assert w['exitCode'] == 0 and not w['timedOut'] and not v['failures']
status = 'installed_native_verified_owner_review_pending'
for mode in ['bare', 'helmet']:
    file = P / (mode + '-manifest.json')
    m = json.loads(file.read_text())
    m['status'] = status
    file.write_text(json.dumps(m, indent=2) + '\n', encoding='utf-8')
(P / 'selection.json').write_text(json.dumps({
    'status': status, 'runtimeInstalled': True, 'fullSetComplete': False,
    'statesPerMode': 12, 'sourceReferences': 144, 'changedFrames': 128,
    'materialChangesOnly': True, 'packageChecks': v['checks'],
    'nativeChecks': n['checks'], 'nativeFailures': n['failures'],
    'actualBerthJourneys': 2, 'exactRegisteredJoins': 32,
    'profileGuard': {'realProfileUnchanged': w['realProfileUnchanged'], 'profileDelta': w['profileDelta']},
    'visualReview': 'All144 registered rest references, four old/new comparisons, lie/sleep head crops, eight standing/walk cards and six actual q0 North berth captures reviewed. Get-up uses reversed original poses. Source-clock GIFs are constructed playback, not native journey videos.',
    'remaining': ['Owner full-motion review', 'Fuller reclining faces versus standing masters require anatomical/perspective review; preservation is not identity proof', 'Protected head/shell unions include nearby shoulder pixels; broad neutral/gold masks are not semantic material segmentation', 'Other bunk rotations/layouts and actual gear changes', 'Full James library and cross-family consistency polish']
}, indent=2) + '\n', encoding='utf-8')

note = '''

## James ordinary rest material continuity — October 1, 2026

Selected james-rest-material-continuity-v1 covers lie-down/sleep/get-up in all
four directions and both gear modes:144 references,128 changed interiors and16
exact standing endpoints. One pooled unique-interior neutral/gold gain per
direction, shared across gear and reversed/aliased poses, replaces standing-only
calibration. Original source bindings and calibration frozen before override.
Alpha, protected head/shell union, geometry, clocks and contact metadata exact;
3600ms sleeping cadence and normal0.8/10.4/0.8s service stages retained.
Broad masks can include gloves/tools/boots and protected unions include nearby
shoulders; this is not semantic shoulder-only correction or head identity proof.

752 package/841 native checks pass;32 exact registered joins. Native scope:
all144 normal loaded references/metadata, eight sleep states for three cycles,
actual retained q0 North berth journeys both gears, two fresh midpoint disk
Continues, fixed contact, exact actor/player/pause/clock/pixels, normal fatigue
100->55 and completion. Engine0/no timeout. Strict owner guard false with only
last_session.json changed, cause unproven; scratch APPDATA and no rollback.
All144 full rest references, four before/after boards, head crops, eight
standing/walk join cards and six actual North berth captures visually reviewed.
Source0 bare/helmet masters already differ at collar/shell pixels; diagnostic
confirms no added differences. Fixture variable and ownership assertion repairs
are archived; no art changed to satisfy them. Reclining faces sometimes appear
fuller than standing masters: anatomical/perspective review remains open.
Other bunk layouts/rotations and locker changes are unproven. Full goal active.
'''
for path in [R / 'docs/CURRENT_STATUS.md', R / 'docs/ASSET_PIPELINE_AND_WORKFLOW.md', R / 'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md', R / 'skills/brinespace-character-pipeline/references/crew-consistency.md', Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data = path.read_bytes()
    if b'## James ordinary rest material continuity' in data:
        continue
    enc = note.encode('utf-8')
    new = enc.lstrip(b'\n') + b'\n' + data if path.name == 'CURRENT_STATUS.md' else data + enc
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    tmp.write_bytes(new)
    os.replace(tmp, path)
(P / 'HANDOFF.md').write_text('''# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: James ordinary rest material

## Objective and acceptance
Continue complete James library/master/style/proportion/material consistency
and cross-family polish. Full goal active; selected revision technically verified,
owner acceptance and full-set quality remain separate.

## Accepted decisions and constraints
Preserve genuine whole-source poses and fixed registration. One pooled material
gain per facing shared across gear/actions; protect head/shell and exact standing
masters. No geometry/alpha/clock/contact changes. Sleep cadence remains3600ms.

## Current state
Paired twelve-state manifests installed after sleep cadence in grid_canvas;
ACTIVE_ASSETS records them. Frozen source-bindings/calibration,144 frame files,
full source review and source-clock previews, six native captures. Source0
ownership diagnostic preserves accepted master collar/shell differences.
Failed fixture versions retained. validate.gd/.uid paired.

## Verification
752 package/841 native checks,0 failures,32 exact registered joins. All144
normal loaded references;8sleep loops three cycles;2actual q0 North berth routes
and fresh mid-sleep disk Continues with exact actor/player/pause/clock/pixels,
normal fatigue55/completion. All144 pose boards, head crops,8standing/walk cards
and6native captures reviewed. Engine0/no timeout. Strict owner delta only
last_session.json,cause unproven; no rollback. Not all bunk/locker contexts.

## Next action
Review fuller reclining faces against master anatomy/perspective before claiming
head identity. Protected regions also include nearby shoulders; material masks
are broad, not semantic. Continue remaining full-source and cross-family review,
actual furniture/gear/travel contexts. No generation/native job live.
''', encoding='utf-8')
print(json.dumps({'status': status, 'packageChecks': v['checks'], 'nativeChecks': n['checks'], 'profileDelta': w['profileDelta']}))
