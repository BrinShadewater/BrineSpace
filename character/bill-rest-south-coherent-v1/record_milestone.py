from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-rest-south-candidate-native-v1'
assert not (P/'candidate-evidence.json').exists(),'Record future revisions separately'
report=json.loads((O/'validation.json').read_text());log=(O/'native.log').read_text();package=json.loads((P/'verification.json').read_text())
assert report['returnCode']==0 and '109 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot'] and package['passed']
summary='''Bill south generic rest candidate — October 1, 2026.
New source exec64f904ac-5ee3-4209-ab66-ef4b9a6fee9e, interiors
execcc9665f2-5239-497d-9e0a-9467e3249287 and corrected recline
exec36d3d557-df4f-417c-b47b-b351486268b2. Bare3states/8 authored entry
poses800ms, exact reversed wake800ms,2 closed-eye supine sleep poses1200ms.
Head north/boots south throughout recline, fixed elevated front camera.
Exact selected south idle,256px/p128,224/H148, fixed per-source rulers
[.30,148/436] and[.16,148/710], master-referenced global matte/hair/face/
bounded shoulder grades. Source frames retain detail rather than flat recolour.
Initial halfway recline projected too tall beside neighbours. Authored correction
reduces projected height via recline; no per-pose normalization. Original source/
prompt and rejected-perspective-review.png retained. Original v2 shallow pose
kept, only corrected right cell fromv3 used; all source hashes/pose order recorded.
9package invariants/109native player checks pass: exact pixels, endpoints,
metadata/density, finite holds, reverse wake and actual sleep clock wrap.
Native148/82 static board reviewed with exact master. Halfway recline improved;
support-arm/torso/face perspective and cadence need continuous motion/full-set
polish. Static comparison does not certify smoothness or owner acceptance.
'''+f'''Runner {report['seconds']}s, overall {report['passed']}; strict profile guard
changes {report['realProfileChanges']}, {report['realProfileFileCount']:,} real
non-log files fingerprinted. Scratch APPDATA used; no owner restoration or
repeat seeking clean profile. Candidate remains unselected; no shared helmet,
compatible physical south rest station, interruption/reward/Continue proof.
Current habitation serves selected east bunk only (prior4rotation audit).
Next south shared helmet, west rest, relevant paired family integration, remaining
meal contexts and complete cross-animation master consistency/motion polish.
Lesson: compare adjacent authoring sources at one game ruler before accepting
them. Correct projected torso/recline in the source; shrinking an entire pose
would conceal the defect and change identity. Keep known-good pose pixels when
an edited multi-pose source also changes an unrelated cell.
Pipeline/bible/maintained and installed skill updated; full goal active.
No normal art selection, game economy, owner layout, export or commit change.
'''
(P/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill south rest\n\n## Objective and acceptance\nFull master-consistent Bill set, then cross-animation polish.\n\n## Accepted decisions and constraints\nExact master idle, fixed rulers and matte materials; preserve selected east bunk and owner saves.\n\n## Current state\nNew authored sources/prompts, deterministic build/manifest/frames/preview/boards, native fixture/UID and scratch runner.\n\n## Verification\n'+summary+'\n## Next action\nSouth helmet, west rest, relevant integration and full-set polish.\n',encoding='utf-8')
files=[p for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
files.extend(O/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
files.extend(R/name for name in ['tests/test_bill_rest_south_candidates.gd','tests/test_bill_rest_south_candidates.gd.uid','tools/run_bill_rest_south_candidate_validation.py'])
hashes={f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
(P/'candidate-evidence.json').write_text(json.dumps({'nativeSubsystemPassed':True,'nativeChecks':109,'packageChecks':9,'strictGuard':report,'normalSelected':False,'visualScope':'static native148/82 board; continuous motion/furniture/owner acceptance separate','sha256':hashes},indent=2)+'\n',encoding='utf-8')
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write('\n\n## Bill south rest candidate — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-south-coherent-v1/HANDOFF.md.\n')
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n\n## Bill south rest candidate — October 1, 2026\n\n'+summary)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south rest candidate — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-south-coherent-v1/HANDOFF.md.\n\n').encode()+status.read_bytes())
print('Recorded south rest:9 package/109 native subsystem checks; strict guard failure retained')
