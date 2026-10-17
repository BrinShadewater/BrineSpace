import hashlib
import json
import subprocess
from pathlib import Path

from milestone_notes import record_guides

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
review = bank / 'release-resume-playtest-v357'
output = root / 'output/james-resume-playtest-v357'
validation = json.loads((output / 'validation.json').read_text())
data = json.loads((review / 'lifecycle-review.json').read_text())
assert validation['exitCode'] == 0 and validation['ownerUnchanged'] and validation['qaOverrideRemoved']
for directory in ['deliverable', 'native-qa']:
    for name, digest in validation['packageHashes'].items():
        with (root / 'output/james-release-closeout-v351' / directory / name).open('rb') as stream:
            assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest
assert data['failures'] == 0 and len(data['cases']) == 4 and len(data['resumes']) == 8
assert all(c['delivered'] and c['siteUnits'] == 2 and c['metal'] == 6 and c['data'] == 1 and c['resumed'] == ['return', 'drain'] for c in data['cases'])
assert all(r['footError'] < .001 and r['cargo'] for r in data['resumes'])
assert (review / 'resume_playtest.gd.uid').exists()
paths = [p.relative_to(root).as_posix() for p in review.glob('*.png')]
assert len(paths) == 4
attrs = subprocess.run(['git', 'check-attr', '--stdin', '-z', 'filter'], input=('\0'.join(paths) + '\0').encode(), capture_output=True, check=True).stdout.split(b'\0')
assert all(attrs[i] == b'lfs' for i in range(2, len(attrs) - 1, 3))
section = f'''### James loaded expedition Continue — October 4, 2026

V357 exact V351 Windows package: {data['checks']} checks, zero failures, four
complete salvage deliveries across all airlock rotations. Eight actual disk saves
read and restored into fresh main scenes through normal RunSave.pending/staged
Continue: each journey interrupted during loaded exterior return and airlock
draining. Route/payload, exact foot contact, tank/helmet, site units and undelivered
resources survive. Continue starts paused; normal selected James player retained.
Every resumed journey completes alive, removes one site unit and delivers exactly
one Metal/one Data once. Four before/after/native-unload boards viewed: no obvious
missing actor/cargo or equipment swap in sampled handoffs.

{len(data['captures'])} native captures, scratch APPDATA, owner folder unchanged,
QA override removed; no game runtime or art edits, no rebuild.
Immediate restored screenshots can catch the deferred Continue camera refocus,
placing the requested crop over the interface (two return cases). Raw captures
retained. Review boards use the next normal simulation frame, 17ms later, after
refocus settles; they do not establish pixel-identical immediate playback.
Earlier V355 fixture setup remains: nearby authored salvage site, scripted starting floor contact/full
tank, controller-driven mission with fixed60Hz updates. This tests fresh-scene disk
Continue, not a process restart or title-button click. Diagnostic last_source may
be overwritten by Architects.pod_for_display after drawing, as recorded in V355;
actual actor snapshots and native images establish resume/equipment checks here.

Loaded exterior checkpoint interruption is now covered in this Windows candidate.
Known coarse cargo quilt/wide North unload stance polish and uninterrupted visual
acceptance remain explicit. No additional stationary proof matrix is needed.
Review: character/james-west-carry-walk-keys-v1/release-resume-playtest-v357/review.json.
Candidate: output/james-release-closeout-v351/deliverable/BrineSpace.exe with PCK.
'''
report = {'version': 357, 'checks': data['checks'], 'failures': 0, 'cases': 4, 'freshSceneDiskResumes': 8, 'ownerUnchanged': True, 'productionChanged': False, 'packageRebuilt': False, 'visualReview': 'Four before/after/native-unload boards viewed; no obvious missing actor/cargo or equipment swap in sampled handoffs.', 'scope': data['scope'], 'remaining': 'Final owner playtest and continuous visual acceptance; coarse cargo quilt and wide North unload stance polish. Process restart and long-session random-world traffic not certified.'}
(review / 'review.json').write_text(json.dumps(report, indent=2) + '\n')
handoff = '''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James loaded Continue

## Objective and acceptance
Finish James and prepare the next release. Loaded exterior disk Continue now
covered; candidate remains ready for final owner playtest within recorded scope.

## Accepted decisions and constraints
Accepted matte art, forward torch, inward tablet and belt wrench preserved.
Owner saves protected; no production changes or publication.

## Current state
New V357 packaged fixture/UID and preparation/run/review/closeout helpers; four
native resume boards plus trace and validation. Existing V351 candidate unchanged.

## Verification
'''+section+'''
## Next action
Final owner playtest of the tested V351 candidate. Avoid more redundant fixtures.
Keep visual polish and uninterrupted acceptance limitations explicit. This frozen
James candidate does not include later concurrent character/UI authoring changes.
'''
(review / 'HANDOFF.md').write_text(handoff)
(output / 'HANDOFF.md').write_text(handoff)
record_guides(root, section, '### James final source review — October 4, 2026')
with (bank / 'HANDOFF.md').open('a', encoding='utf8') as stream:
    stream.write('\n' + section)
f = bank / 'material-repair-progress.json'
old = f.read_bytes()
ledger = json.loads(old)
ledger['releaseLoadedExpeditionContinue'] = report
assert f.read_bytes() == old
f.write_text(json.dumps(ledger, indent=2) + '\n')
f = root / 'docs/JAMES_RELEASE_CLOSEOUT.md'
old = f.read_bytes()
text = f.read_text().replace('Random-world dispatch ecology, long-session traffic and loaded exterior checkpoint interruption not certified.', 'V357 adds eight loaded-return/drain disk checkpoints restored into fresh scenes; all four journeys deliver once. Random-world dispatch ecology, process restart and long-session traffic not certified.')
assert f.read_bytes() == old
f.write_text(text)
print(json.dumps(report))
