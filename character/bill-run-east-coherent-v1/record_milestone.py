from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];A=P.parent/'bill-locomotion-master-audit-v1'
assert not (P/'runtime-evidence.json').exists(),'Preserve dated candidate evidence'
out=R/'output/bill-run-east-candidate-native-v1';report=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text()
assert report['returnCode']==0 and '36 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot']
package=json.loads((P/'verification.json').read_text());assert package['passed'] and package['checks']==21
summary='''Bill run source audit and east candidate — October 1, 2026.
Fixed1:1 native-density master comparison covers8 original cardinal run rows:
bare and equipment each4directions. Old run helmets differ visibly from current
closed shared helmets; frontal run build reads broader than selected idle.
Initial independently fitted thumbnails falsely exaggerated scale differences;
corrected board uses declaredH148/native pixels and common physical foot baseline.
Current Bill animation_state uses walk for locomotion; main copies that state.
Old _choose_walker_motion_state run chooser has no calling references in scripts.
Full library run coverage remains required, but no current NPC running behavior
or run reachability acceptance is claimed and gameplay speed is unchanged.
New East candidate sources: rejected6pose run-v1 exec8065aa35-d3ad-4886-ab48-e47269f9b39c
and run-v2 exec88dc9787-dff8-46c3-88d4-b78adab0edf2 repeat leading limbs/arm silhouettes.
Retain both prompts and sources as rejected evidence, not selected motion.
New3pose half exec5e6a257e-7b8d-42c4-bfe3-fbcfa6e5568d and complementary3pose
execbfceaef4-b360-4e24-8dc3-f195c4a5aa54 provide6 distinct candidates with arm
silhouette variation. Exact prompts retained. Source anatomy ruler148/610 across
BOTH triptychs, no per-pose stretch, pelvis-axis X registration/shared source
baseline820; pooled neutral quantile grade and face/hair/burgundy gains reference
the selected East idle. Shared256/p128,224/H148,6phases/540msloop and explicit
run-east .168cell stride retained for candidate movement-distance playback.
21 packaging checks and36 actual-player native checks pass: exact pixels,
metadata, source timing, movement-distance phase, loop wrap and stationary hold.
Fresh1792x512 native148/82 board reviewed; browser master comparison loads6poses.
Candidate remains staged; normal loader/ACTIVE_ASSETS unchanged by this milestone.
Fine leg/arm side layering and counter-swing, flight/readable running cadence,
idle-to-run lean/face/detail, native shared helmet fit, cardinal directions,
diagonal walk and whole-set consistency remain open. Distinct hashes do not prove
biomechanics or smooth motion. Face appears slightly darker in candidate preview
and needs local review, not a whole-body exposure change.
'''+f'''Native engine0/clean/fresh capture, {report['seconds']}s scratch APPDATA.
Strict overall passed=False: owner-profile guard changed {report['realProfileChanges']}
among {report['realProfileFileCount']:,} non-log files. Attribution unproven;
failed guard retained, no owner restore or repeat for clean interval.
Previous goal turn made substantive progress: helmet torch12states selected with
236package/395native checks and recorded evidence; full goal remains active.
No commit/export; concurrent files preserved. PNG LFS filter confirmed.
Lesson: compare different canvas profiles at fixed anatomical density, not
independent thumbnails. Reject repeated leading-limb sheets; smaller directional
half-cycle authoring can clarify required arm silhouettes, but source variation
must still pass anatomical and motion review before normal selection.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill run family

## Objective and acceptance
Finish full master-consistent Bill set and cross-animation anatomy/material/camera/motion polish.

## Accepted decisions and constraints
Selected directional masters, fixed anatomical scale, native shared helmet; preserve gameplay and owner profile. Existing reversible work authorized.

## Current state
New bill-locomotion-master-audit-v1 fixed-density review/script/hashes. New bill-run-east-coherent-v1 four sources/prompts (first2 rejected), six candidate exports/build/registration/preview/verification. Native candidate fixture+UID/scratch runner. No new normal selection.

## Verification
'''+summary+'''
## Next action
Review/refine run limb-side layering and cadence/face against master, fit native East helmet, then independently author West/North/South runs and diagonal walk; full-set polish afterward.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');(A/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[f for folder in [P,A] for f in folder.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
files += [out/n for n in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png']]
files += [R/n for n in ['tests/test_bill_run_east_candidate.gd','tests/test_bill_run_east_candidate.gd.uid','tools/run_bill_run_east_candidate_validation.py','scripts/bill_npc.gd','scripts/main.gd']]
(P/'runtime-evidence.json').write_text(json.dumps({'normalSelected':False,'candidateNativeSubsystemPassed':True,'nativeChecks':36,'packageChecks':21,'strictGuard':report,'normalRunningReachabilityProven':False,'currentFileSha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill run audit and East candidate — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-run-east-coherent-v1/HANDOFF.md.\n'
for n in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/n).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded21 package/36 candidate native checks; strict guard failure and staged status retained')
