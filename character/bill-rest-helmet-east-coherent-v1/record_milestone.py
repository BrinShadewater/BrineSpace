from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-rest-helmet-east-candidate-native-v1'
assert not (P/'candidate-evidence.json').exists(),'Future revisions need separate evidence'
report=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text();package=json.loads((P/'verification.json').read_text())
assert report['returnCode']==0 and '109 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot'] and package['passed']
summary='''Bill east shared-helmet rest candidate — October 1, 2026.
Paired lie-down/sleep/get-up retains selected equipped idle exactly and native
35x38 east hardware component at scale1 through seven registered neck/tilt fits.
Bare bodies/timelines remain identical outside bounded head/helmet regions.
Authored closed-eye donor exec43de739f-b7d9-495b-b277-72833aa65c4b contributes
only9RGB pixels to canonical visible eye; alpha, shell, lights, visor, beard and
face outline outside mask exact. Preserve original source/prompt and bounded
component extraction. Rotation alone still needs perspective/neck polish in
later whole-set passes; native component match does not certify foreshortening.
28 package invariants and109 native player checks pass, exact pixels/timing/
endpoints/density/metadata and finite reverse wake/loop player wrap. Native148/82
board and enlarged closed-eye comparison reviewed. Live preview loaded via CUA;
470ms lie/330ms wake scrub alignment inspected, sleep canvas advancing observed.
These are sampled screenshots, not continuous motion smoothness acceptance.
Preview heading's Windows default-codepage artifact fixed by explicit UTF-8 read;
reloaded browser confirms heading. No runtime source change for that repair.
'''+f'''Strict runner overall {report['passed']}, {report['seconds']}s; changes
{report['realProfileChanges']}, {report['realProfileFileCount']:,} real non-log
files fingerprinted. Scratch APPDATA used, failed guard retained; no restoration
or repeat to seek a clean interval. Paired candidate remains unselected normally.
No actual bed contacts/occlusion/interrupt/Continue proof, and specialised east
Bill bunk stays selected. Next prioritize north rest with actual rest-head target,
then south/west and paired family physical integration. Master identity, torso
width, subtle breathing/cadence and all cross-animation joins remain full-polish
work. Meals/inspection contexts also remain; full goal active, no export/commit.
Lesson: wearable sleep expression is a bounded authored RGB change, not a new
helmet. Keep per-pose native component ruler fixed and verify paired bodies;
screen samples supplement but cannot replace live motion/contact acceptance.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill paired east rest\n\n## Objective and acceptance\nFull master-consistent animation set and cross-animation polish.\n\n## Accepted decisions and constraints\nExact master/idle/shared equipment, native scale, owner geometry/saves preserved.\n\n## Current state\nNew helmet build, authored eyelid source/prompt and bounded component,3-state manifest, frames, native fixture/UID, scratch runner, boards and working preview. Bare east candidate remains paired.\n\n## Verification\n'+summary+'\n## Next action\nNorth actual-rest-head choreography; remaining headings and physical paired integration.\n'
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files.extend(O/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
files.extend(R/name for name in ['tests/test_bill_rest_helmet_east_candidates.gd','tests/test_bill_rest_helmet_east_candidates.gd.uid','tools/run_bill_rest_helmet_east_candidate_validation.py'])
hashes={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'candidate-evidence.json').write_text(json.dumps({'nativeSubsystemPassed':True,'nativeChecks':109,'packageChecks':28,'strictGuard':report,'normalSelected':False,'visualScope':'native148/82 board and eyelid review; browser intermediate scrub samples; continuous motion/contact unproven','sha256':hashes},indent=2)+'\n',encoding='utf-8')
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write('\n\n## Bill paired east rest candidate — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-helmet-east-coherent-v1/HANDOFF.md.\n')
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n\n## Bill paired east rest candidate — October 1, 2026\n\n'+summary)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill paired east rest candidate — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-helmet-east-coherent-v1/HANDOFF.md.\n\n').encode('utf-8')+status.read_bytes())
print('Recorded paired east rest:28 package/109 native checks; strict guard failure retained')
