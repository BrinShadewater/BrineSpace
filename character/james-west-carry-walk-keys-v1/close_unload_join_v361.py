import json
import subprocess
from pathlib import Path
from milestone_notes import insert_status

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
out = bank / 'north-unload-join-audit-v361'
report = json.loads((out / 'evidence.json').read_text())
assert len(report['sourceSamples']) == 14 and len(report['nativeJoinSamples']) == 4
media = sorted(out.glob('*.png'))
for path in media:
    result = subprocess.run(['git', 'check-attr', 'filter', '--', str(path.relative_to(root))],
                            capture_output=True, text=True, check=True)
    assert result.stdout.rstrip().endswith(': lfs'), result.stdout
report.update({
    'sourceBoardViewed': True, 'nativeBoardViewed': True,
    'disposition': 'Excluded from current release; preserved unselected study.',
    'findings': [
        'Reversed lowering retains carrying arms until the final relaxed-arm source; suit/hardware detail changes at that join.',
        'Accepted baseline also uses a discrete final crouch-to-standing rise; no claim that baseline is continuously smooth.',
        'Existing persistent floor-case admission requires West-facing, exact approved release artwork. North lifecycle completion alone establishes no persistent prop.',
        'North prop support would require an authored release cue and registered case geometry, followed by interruption/save verification; inventing a cue is outside this diagnostic.'
    ],
    'normalChanged': False, 'packageChanged': False, 'newGenerationJobs': 0,
    'limits': '14 preserved source samples and 20 preserved native endpoint captures viewed. No uninterrupted playback acceptance or new simulation. Candidate has no helmet counterpart.',
    'next': 'Use exact V358 Windows ZIP for final owner playtest. Retain North material/stance and ending join as explicit deferred polish.'
})
(out / 'evidence.json').write_text(json.dumps(report, indent=2) + '\n')
section = '''### James North unload endpoint review — October 4, 2026

V361 preserved-source endpoint comparison:14 source samples and20 corrected-linear
native captures across four workshop layouts, both boards viewed. V360 reversal
retains carrying arms before the relaxed-arm endpoint and changes suit/hardware
detail. Excluded from current release, study preserved unselected. Accepted baseline
also has a discrete final rise; this is not a claim of smooth baseline continuity.
West-only existing floor-case cue remains unchanged; North lifecycle completion
does not prove case deposit. Do not fabricate a North release from a pose index.
No new generation, simulation, art admission, runtime change or package rebuild.
Exact V358 Windows ZIP stays ready for final owner playtest; material/stance/ending
join polish remains explicit. Evidence: character/james-west-carry-walk-keys-v1/
north-unload-join-audit-v361/evidence.json; docs/JAMES_RELEASE_CLOSEOUT.md updated.
'''
insert_status(root / 'docs/CURRENT_STATUS.md', section,
              '### James staged north unload chain — October 4, 2026')
handoff = '''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James unload release decision

## Objective and acceptance
Finish James animations and prepare the next game version. Preserve owner-selected
motion; keep known source polish separate from tested release integration.

## Accepted decisions and constraints
Matte original master, forward torch, inward diagnostics tablet, belt wrench,
stable height/helmet. V351/V358 tested selection and portable package retained.

## Current state
V361 source/native endpoint comparison boards and evidence.json, reproducible audit
and closeout helpers. docs/JAMES_RELEASE_CLOSEOUT.md and CURRENT_STATUS.md updated.
V359/V360 North studies remain unselected and excluded from this release.

## Verification
14 preserved source samples and20 preserved corrected-linear native captures viewed.
Carrying-to-neutral arm/suit join remains discontinuous. Baseline also has a discrete
final rise. No approved North persistent-case release cue exists; no guessed prop
timing or geometry added. Two new review images covered by Git LFS. No new generation,
simulation, runtime change or package rebuild. V360's1102checks0 remain scoped to
fixture lifecycle completion, not continuous visual or persistent-case acceptance.

## Next action
Final owner playtest of output/james-windows-package-v358/
BrineSpace-Windows-James-2026-10-04.zip. Preserve explicit North material/stance/join
polish. Revisit source coherence before helmet fitting or floor-case extension.
'''
(out / 'HANDOFF.md').write_text(handoff, encoding='utf8')
ledger = bank / 'material-repair-progress.json'
if ledger.exists():
    data = json.loads(ledger.read_text())
    data['northUnloadEndpointReview'] = report
    ledger.write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({'sourceSamplesViewed':14,'nativeSamplesViewed':20,
    'releaseDisposition':'retain accepted version','newGenerationJobs':0,
    'normalChanged':False,'packageChanged':False,'lfsReviewImages':len(media)}))
