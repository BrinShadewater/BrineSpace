from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-rest-east-candidate-native-v1'
assert not (P/'candidate-evidence.json').exists(),'Record later revisions separately'
report=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text()
assert report['returnCode']==0 and '108 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot']
summary='''Bill east generic rest candidate — October 1, 2026.
New bare lie-down/sleep/get-up source preserves selected idle entry exactly,
256px/p128,224/H148 density, matte charcoal detail, muted burgundy and brown hair.
Initial source switched leg direction at reclining: retained, rejected for motion.
Authored v2 holds head-left/boots-right through seated/reclined poses, matching
legacy east sleep. Two independently authored v3 lowering interiors bridge the
large standing-to-seated jump. One fixed XY ruler per independent source, never
normalize lowered bounds to standing height; global atlas material grades use
the same selected idle authority.8 entry poses/800ms, exact reverse wake/800ms,
2 relaxed sleep poses/1200ms loop with exact entry/sleep/wake endpoints.
9 package invariants and108 actual-player native checks pass. Native148/82 pose
board visually reviewed against exact idle; lowering choreography improves,
but cross-source torso/arm detail, perspective and two-pose breathing need finer
motion polish. Static board review is not live motion or furniture acceptance.
First native test incorrectly used finite frame_at_elapsed to test loop wrap;
that API deliberately clamps. Corrected test exercises actual frame clock.
Failed108-check/1-failure report retained in interval-before archive.
'''+f'''Corrected native run {report['seconds']}s; overall {report['passed']} because
strict owner profile guard reports {report['realProfileChanges']}; all
{report['realProfileFileCount']:,} non-log files fingerprinted. Scratch APPDATA
used; no owner restoration or retry for clean guard. No normal runtime selection,
helmet version, station geometry/occlusion, interruptions or Continue proof yet.
Existing specialised Bill east bunk sequence remains selected. Other generic
rest directions, meal transition integration and full-set polish remain open.
Next: review moving east cadence/master proportions, fit shared helmet, prove
actual generic rest contacts, then expand headings and integrate paired family.
No gameplay/economy/layout changes, export or commit; full goal remains active.
Lesson: fix an authored directional discontinuity before frame extraction;
bridge major pose gaps with authored anatomy. Loop proof must call the looping
player; finite frame lookup cannot prove wrap behavior.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill east generic rest\n\n## Objective and acceptance\nFinish full master-consistent Bill set, then cross-animation polish.\n\n## Accepted decisions and constraints\nExact master/idle, fixed per-source ruler, matte grade, preserve selected bunk and owner saves.\n\n## Current state\nNew source/prompts, deterministic build,3-state candidate manifest, frames, comparison boards, preview, native fixture/UID and scratch runner.\n\n## Verification\n'+summary+'\n## Next action\nLive motion review and identity joins; helmet and physical rest integration, other directions.\n'
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files.extend(O/name for name in ['native.log','validation.json','profile-before.json','profile-after.json','loaded-water-carry.png'])
for archive in O.glob('interval-before-*'):files.extend(p for p in archive.iterdir() if p.is_file())
files.extend(R/name for name in ['tests/test_bill_rest_east_candidates.gd','tests/test_bill_rest_east_candidates.gd.uid','tools/run_bill_rest_east_candidate_validation.py'])
hashes={str(f.relative_to(R)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'candidate-evidence.json').write_text(json.dumps({'nativeSubsystemPassed':True,'nativeChecks':108,'packageChecks':9,'strictGuard':report,'visualScope':'static native148/82 board reviewed; live motion not yet reviewed','normalSelected':False,'sha256':hashes},indent=2)+'\n')
for target in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/target).open('a',encoding='utf-8') as f:f.write('\n\n## Bill east generic rest candidate — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-east-coherent-v1/HANDOFF.md.\n')
mirror=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
with mirror.open('a',encoding='utf-8') as f:f.write('\n\n## Bill east generic rest candidate — October 1, 2026\n\n'+summary)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east generic rest candidate — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-east-coherent-v1/HANDOFF.md.\n\n').encode()+status.read_bytes())
print('Recorded bare east rest candidate:108 native subsystem checks; strict profile guard failure retained')
