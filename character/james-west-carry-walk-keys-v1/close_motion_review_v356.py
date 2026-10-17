import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from milestone_notes import record_guides

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
review = bank / 'release-motion-review-v356'
catalogue = json.loads((review / 'playback.json').read_text())
observations = json.loads((review / 'browser-observations.json').read_text())
samples = [o for o in observations if 'scale' not in o]
assert len(catalogue) == 22 and len(samples) == 66
assert Counter(o['family'] for o in samples) == Counter({k: 3 for k in catalogue})
assert (review / 'playback.json').read_bytes() == (bank / 'release-motion-review-v348/playback.json').read_bytes()
paths = [p for rows in catalogue.values() for row in rows for p in row['paths']]
missing = [p for p in paths if not (root / p.lstrip('/')).is_file()]
assert not missing
assert 'Paused / 40 ms' in (review / 'step-control-state.txt').read_text()
assert 'Playing / ' in (review / 'playing-control-state.txt').read_text()
rasters = [p.relative_to(root).as_posix() for p in review.glob('*.png')]
assert len(rasters) == 69
attrs = subprocess.run(['git', 'check-attr', '--stdin', '-z', 'filter'], input=('\0'.join(rasters) + '\0').encode(), capture_output=True, check=True).stdout.split(b'\0')
assert all(attrs[i] == b'lfs' for i in range(2, len(attrs) - 1, 3))
package = root / 'output/james-release-closeout-v351/deliverable'
expected = {'BrineSpace.exe': '7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76', 'BrineSpace.pck': '13483c405aa1c6e0c070b216882e71138fc5b3f8c7131f306db32d77ca706510'}
for name, digest in expected.items():
    with (package / name).open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == digest

section = '''### James final source review — October 4, 2026

V356 review-only browser update: pause/seek and 40ms stepping added, V348 selected
playback data byte-identical. All 22 catalogue groups reviewed at three elapsed
times in enlarged 148px view, all supplied directions and both equipment variants
shown together. 66 saved browser screenshots actually viewed; three additional
diagnostic screenshots viewed at 82/54/27px. No new major defect apparent in these
samples: connected limbs, stable equipment and matte palette; diagnostics retain
the inward tablet and belt wrench. Cargo coarse quilt and wide North unload stance
remain known polish, not fixed. All referenced files present, all 69 screenshot
rasters covered by Git LFS. Step control reached paused40ms; Play visibly advanced.

This is sampled source review, not uninterrupted observation or every-frame flash
certification. Common elapsed times may reach different frame indices/endpoints
for different directions. Native furniture, cargo, survival/refuge and exterior
integration evidence remains V349–V355, with its recorded fixture limits. No game
runtime or production artwork changed; exact tested V351 EXE/PCK hashes unchanged.
No owner-save access or Godot probe was needed for this review-only change.

Functional Windows closeout checks are complete within their recorded scope; the
local candidate is ready for final owner playtest. Do not add another stationary
proof matrix. Final continuous visual acceptance and known material/stance polish
remain explicit; the full original-master art goal is not certified complete.
Review: character/james-west-carry-walk-keys-v1/release-motion-review-v356/index.html.
Candidate: output/james-release-closeout-v351/deliverable/BrineSpace.exe, PCK alongside.
'''
report = {'version': 356, 'groups': 22, 'enlargedScreenshots': 66, 'gameScaleScreenshots': 3, 'missingPaths': missing, 'selectedPlaybackUnchanged': True, 'productionChanged': False, 'packageHashesUnchanged': True, 'rasterLfs': 69, 'finding': 'No new major defect apparent in viewed samples.', 'limits': 'Three elapsed samples per group, not every-frame or uninterrupted motion certification. Coarse cargo quilt and wide North unload stance remain polish.', 'next': 'Final owner playtest of the tested Windows candidate; no further stationary proof matrix.'}
(review / 'review.json').write_text(json.dumps(report, indent=2) + '\n')
handoff = '''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James final source review

## Objective and acceptance
Finish James and prepare the next game version. Functional Windows checks complete
within recorded fixture scope; candidate ready for final owner playtest.

## Accepted decisions and constraints
Accepted original art, matte palette, forward torch, inward tablet and belt wrench
retained. Cargo quilt and North unload stance polish explicitly unresolved.

## Current state
V356 review-only HTML with seek/step control, unchanged selected catalogue,
69 browser screenshots and observation/report files. Production and V351 package
unchanged. Local browser remains on the review at 82px, playing diagnostics.

## Verification
'''+section+'''
## Next action
Final owner playtest using output/james-release-closeout-v351/deliverable/BrineSpace.exe
with its PCK alongside. No publication performed. Continuous visual acceptance,
random-world/long-session traffic, Mac gameplay and original fine-quilt material
are not certified by these checks; avoid treating those limits as new regressions.
'''
(review / 'HANDOFF.md').write_text(handoff)
record_guides(root, section, '### James packaged exterior expeditions — October 4, 2026')
with (bank / 'HANDOFF.md').open('a', encoding='utf8') as stream:
    stream.write('\n' + section)
ledger_path = bank / 'material-repair-progress.json'
old = ledger_path.read_bytes()
ledger = json.loads(old)
ledger['finalSourceReview'] = report
assert ledger_path.read_bytes() == old
ledger_path.write_text(json.dumps(ledger, indent=2) + '\n')
checklist = root / 'docs/JAMES_RELEASE_CLOSEOUT.md'
old = checklist.read_bytes()
text = '''# James release closeout

Updated October 4, 2026. The tested local Windows candidate is ready for final
owner playtest. Preserve accepted animations; do not expand the set or restart
unsuccessful material-generation studies during release closeout.

| Area | Evidence | Limits / known polish |
|---|---|---|
| Selected source animations | V348 selected-loader coverage, V356 three elapsed samples per each of 22 groups; all supplied directions/both equipment variants, 66 enlarged screenshots plus three game-scale diagnostic screenshots viewed. No new major defect apparent in samples. | Sampled source review does not certify every frame or uninterrupted playback. Coarse cargo quilt and wide North unload stance remain polish. |
| Tools and cargo | Accepted forward torch work, inward tablet diagnostics, wrench stays on belt. V352 packaged workshop lifecycle: eight layout/gear cases, 1104 checks, 1074 native captures, eight boards viewed. | Observed West/South carry to North unload; source coverage covers other directions. |
| Turns | Selected turns and joins present; V356 start/intermediate/late samples across four turn groups retain connected legs and stable scale. | Different direction clocks reach different frames at common sample times; continuous visual acceptance remains for owner playtest. |
| Rest and furniture | V350: 497 checks, 16 actual habitation/lounge layout/gear cases, 112 native captures, eight boards viewed. Entry, held-rest actor restore, finite power-loss exit pass. | First registered station per layout checked; autonomous arrival and whole-run rest checkpoint not established. |
| Survival and refuge | V349 source death dispatch; V353 packaged survival: 2290 checks, 16 direction/gear/outcome cases. V354 controller-selected refuge: 826 checks, eight direction/gear cases, natural recovery. | Controlled flooding and initial reserves; fixture limits recorded in each review. |
| Swimming and expeditions | V347 normal gameplay swimming repair installed; clearance/transition checks, native tests, two disk resumes, crew regression pass. V355 packaged normal exterior dispatch: 15735 checks, four complete salvage deliveries across airlock rotations, twelve phases, 1550 native captures. | Nearby fixture-created site; fixed-time stepping. Random-world dispatch ecology, long-session traffic and loaded exterior checkpoint interruption not certified. |
| Playable release | V351 Windows candidate brinespace-5024faab0e485c1a: frozen inputs, maintained exporter, package audit and actual release New Game/Continue/F8 checks. Exact EXE/PCK hashes unchanged through V356. | Local candidate; no upload, Mac gameplay acceptance or long-session memory certification. Fixture exit ObjectDB leak warnings remain recorded. |

Functional Windows closeout is complete within the recorded scope. The full
original-master art goal is not certified complete: continuous visual acceptance
and material/stance polish remain explicit, rather than being described as fixed.

Next action: final owner playtest of
output/james-release-closeout-v351/deliverable/BrineSpace.exe, with PCK alongside.
Use release-motion-review-v356 for targeted visual feedback. Do not spend another
sequence of turns adding stationary proof to the same completed integration cases.
'''
assert checklist.read_bytes() == old
checklist.write_text(text)
print(json.dumps(report))
