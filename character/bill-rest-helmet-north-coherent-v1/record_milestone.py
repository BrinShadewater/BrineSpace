from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-rest-helmet-north-candidate-native-v1'
assert not (P/'candidate-evidence.json').exists(),'Record later revisions separately'
report=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text();package=json.loads((P/'verification.json').read_text())
assert report['returnCode']==0 and '110 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot'] and package['passed']
summary='''Bill paired north rest candidate — October 1, 2026.
3 shared-helmet states/8 finite entry slots, exact reverse wake and2 sleep slots.
Exact selected equipped north idle. Early lowering uses native35x36 rear canonical
head; later kneel/prone frames reuse authored rear-shell perspective components
from bill-death-ground-helmet-north-coherent-v1 (exec43b98351-45f2-44a6-878e-203e2e75c72e),
same fixed [.35,.36] source ruler and saved master matte curve. Original source
and exact prompt copied locally, source/authority hash checked. No new body art
or generated facial expression: rear face remains hidden. Paired body pixels
outside declared equipment region/timing/pivots/density unchanged. Both settled
sleep poses hold identical component4 and registered position, avoiding helmet
projection changes during body breathing.28 package checks/110 native player
checks pass. Native148/82 static board reviewed against equipped idle and bare
rest; neckline/perspective/detail/cadence still need full-set motion polish.
'''+f'''Runner {report['seconds']}s, overall {report['passed']}; strict profile guard
changes {report['realProfileChanges']}, {report['realProfileFileCount']:,} real
non-log files fingerprinted, scratch APPDATA. Failed guard retained; no clean
interval retry or owner restoration. Paired north remains staged: current
habitation offers specialised east Bill bunk only in all4 rotations. No north
physical station/route/interrupt/Continue proof or normal selection claim.
Next south/west rest, paired family integration where appropriate, remaining
meal contexts and full cross-animation master consistency/polish. Goal active.
Lesson: reuse hash-bound authored wearable pitch components when the anatomical
view matches; copying the donor body is unnecessary. Keep the same hardware
projection/placement across subtle breathing poses; validate paired body pixels
independently. Component matching and static review do not prove live smoothness.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill paired north rest\n\n## Objective and acceptance\nFull master-consistent Bill set, then cross-animation polish.\n\n## Accepted decisions and constraints\nExact selected masters, native equipment size, fixed source ruler/matte grade; preserve owner saves and selected east bunk.\n\n## Current state\nHelmet sources/prompt, deterministic component fitting,3-state manifest/frames/preview, package verifier, native fixture/UID and scratch runner. Normal selection remains unchanged.\n\n## Verification\n'+summary+'\n## Next action\nSouth/west rest, relevant integration and full-set polish. No commit/export.\n'
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files.extend(O/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
files.extend(R/name for name in ['tests/test_bill_rest_helmet_north_candidates.gd','tests/test_bill_rest_helmet_north_candidates.gd.uid','tools/run_bill_rest_helmet_north_candidate_validation.py'])
hashes={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'candidate-evidence.json').write_text(json.dumps({'nativeSubsystemPassed':True,'nativeChecks':110,'packageChecks':28,'strictGuard':report,'normalSelected':False,'visualScope':'native148/82 static board; no live motion/physical north station proof','sha256':hashes},indent=2)+'\n',encoding='utf-8')
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write('\n\n## Bill paired north rest — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-helmet-north-coherent-v1/HANDOFF.md.\n')
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n\n## Bill paired north rest — October 1, 2026\n\n'+summary)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill paired north rest — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-helmet-north-coherent-v1/HANDOFF.md.\n\n').encode()+status.read_bytes())
print('Recorded north helmet rest:28 package/110 native subsystem checks; strict guard failure retained')
