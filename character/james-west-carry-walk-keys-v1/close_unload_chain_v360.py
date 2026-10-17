import hashlib
import json
import subprocess
from pathlib import Path

from milestone_notes import record_guides

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
review = bank / 'north-unload-chain-v360'
output = root / 'output/james-unload-playtest-v360'
validation = json.loads((output / 'validation.json').read_text())
native = json.loads((review / 'native-review.json').read_text())
assert validation['exitCode'] == 0 and validation['ownerUnchanged'] and validation['qaOverrideRemoved']
assert native['failures'] == 0 and len(native['cases']) == 4 and all(c['completed'] for c in native['cases'])
for name, digest in validation['packageHashes'].items():
    with (root / 'output/james-release-closeout-v351/deliverable' / name).open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest
tasks = {part: json.loads((review / part / 'generation.json').read_text()) for part in ['bend', 'rise']}
assert all(t['status'] == 'Success' for t in tasks.values())
assert (review / 'native_playtest.gd.uid').exists()
paths = [p.relative_to(root).as_posix() for p in review.rglob('*') if p.suffix in ['.png', '.mp4']]
attrs = subprocess.run(['git', 'check-attr', '--stdin', '-z', 'filter'], input=('\0'.join(paths) + '\0').encode(), capture_output=True, check=True).stdout.split(b'\0')
assert all(attrs[i] == b'lfs' for i in range(2, len(attrs) - 1, 3))
report = {'version': 360, 'selected': False, 'normalChanged': False, 'packageChanged': False, 'rawSources': {part: {'taskId': t['task_id'], 'status': t['status']} for part, t in tasks.items()}, 'estimatedUSD': sum(t['estimatedUSD'] for t in tasks.values()), 'billingVerified': False, 'generatedRiseDisposition': 'Rejected: additional downward dip, head shape drift and pink flash visible in raw frames around 38–52.', 'candidateMethod': '142-frame lowering source forward then explicit reversed indices140..0, plus existing standing endpoint;520ms. Exact selected entry/end textures in native fixture. No RGB repaint, body warp or independent per-frame normalization.', 'chronologyReview': 'All twelve alpha chronology boards and one raw rise board viewed;284 raw source poses. Five enlarged browser timestamps viewed for reversal chain.', 'nativeChecks': native['checks'], 'nativeFailures': 0, 'nativeCases': 4, 'nativeCaptures': len(native['captures']), 'nativeReview': 'Four corrected-linear-filter workshop boards viewed. Normal routed workshop lifecycle completes and candidate terminal slot283 actually rendered. Native APNGs supplied, not continuously observed by agent.', 'ownerUnchanged': True, 'rasterMediaLfs': len(paths), 'limits': 'Bare North fixture-only candidate. Texture/material/master consistency, carrying-arm release, full endpoint continuity, helmet fit and persistent case visibility remain unproven. Existing cosmetic floor-case observer admits West only, so completion of the activity does not prove a persistent North floor prop.', 'next': 'Resolve floor-case visibility and the arm/standing join in the candidate; then fit/review helmet counterpart before any normal admission. No further uncontrolled generation retries.'}
(review / 'review.json').write_text(json.dumps(report, indent=2) + '\n')
section = f'''### James staged north unload chain — October 4, 2026

V360 two controlled Hailuo02 first/last jobs, 142frames each, US$0.56 estimated
total/billing unverified. Exact controls/prompts/hashes and raw clips preserved.
Generated rise REJECTED: extra downward dip, head drift and pink flash visible in
raw source around frames38–52. All12alpha chronology boards and one raw rise board
viewed. Candidate instead reuses complete lowering forward/reversed140..0 then
existing standing endpoint;284slots,520ms, no RGB repaint/body warp/individual
frame normalization. Five148px browser timestamps reviewed. Candidate remains
UNSELECTED; lowering still changes cloth/hardware/head detail from original master.

Corrected fixture-only native substitution in exact V351 Windows package:
{native['checks']}checks0, four actual workshop layouts/bare North unload,
{len(native['captures'])}native captures (60Hz during arrival/unload,10Hz otherwise).
Normal route/activity/arrival and terminal candidate slot283 exercised. Four boards
viewed; no obvious actor clipping or disappearance in those samples. Exact selected
entry/end textures retained. First nearest-filter/missing-metadata fixture evidence
preserved under output/james-unload-playtest-v360/initial-nearest-filter-setup and
excluded from final rendering claims. Corrected candidate copies normal texture
metadata, recomputes its own alpha extent and uses normal linear filtering.
Scratch APPDATA, owner unchanged; QA override removed, EXE/PCK hashes unchanged.
All {len(paths)}new source/review media files covered by Git LFS.

Case persistence is NOT established: existing checkpoint_floor_state_v2.release_time
requires a West-facing return plan, while this activity faces North. Idle completion
and retained endpoint artwork do not prove a visible persistent North floor case.
Reversed carrying-arm posture, final standing join, original-master material and
helmet counterpart remain gates before admission. No runtime/art bank edit, rebuild,
or installation. Native APNGs supplied; not continuously observed by agent.
Review: north-unload-chain-v360/reversal.html and review.json.
'''
handoff = '''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James north unload chain

## Objective and acceptance
Finish James animations. Full bare North unload candidate now packaged and exercised
in actual workshop lifecycle; persistent case, joins/material and helmet remain open.

## Accepted decisions and constraints
Existing tested V351/V358 selection preserved. Forward cargo, belt wrench, matte
original master and physically registered motion remain required.

## Current state
V360 raw clips/metadata, full extractions, explicit reversal catalogue/APNGs, browser
comparison, native fixture/UID, four native boards/APNGs and preparation/run/review
helpers. Generated rise rejected; no normal runtime or production asset changes.

## Verification
'''+section+'''
## Next action
Fix staged North floor-case handoff and check carrying-arm/final neutral joins.
Then helmet fitting/review, before admission. Avoid more blind generation retries.
Current exact tested Windows ZIP remains output/james-windows-package-v358/.
'''
(review / 'HANDOFF.md').write_text(handoff)
(output / 'HANDOFF.md').write_text(handoff)
record_guides(root, section, '### James north unload stance study — October 4, 2026')
with (bank / 'HANDOFF.md').open('a', encoding='utf8') as stream:
    stream.write('\n' + section)
f = bank / 'material-repair-progress.json'
old = f.read_bytes()
ledger = json.loads(old)
ledger['northUnloadChainStudy'] = report
assert f.read_bytes() == old
f.write_text(json.dumps(ledger, indent=2) + '\n')
print(json.dumps({'version': 360, 'nativeChecks': native['checks'], 'nativeFailures': 0, 'cases': 4, 'normalChanged': False, 'ownerUnchanged': True, 'mediaLfs': len(paths), 'estimatedUSD': .56}))
