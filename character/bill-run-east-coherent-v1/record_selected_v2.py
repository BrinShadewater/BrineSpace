from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
assert not (P/'selected-evidence-v2.json').exists(),'Keep revisions separate'
reports={}
for key,folder,count in [('candidate','bill-run-east-candidate-native-v1',70),('normal','bill-run-east-selected-native-v2',73)]:
 out=R/'output'/folder;report=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text();assert report['returnCode']==0 and f'{count} checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot'];reports[key]=report
package=json.loads((P/'verification.json').read_text());helmet=json.loads((P/'helmet-verification.json').read_text());assert package['passed'] and helmet['passed']
summary='''Bill paired East run selected, face v2 — October 1, 2026.
Previous goal turn made progress: eight fixed-density run/master audit rows and
six independently authored East run candidates, with native clock evidence.
Skin authority mistakenly included beard and had gain~.48R/.44G/.42B, darkening
the animated face. Restrict master skin to warm visible face with luminance>65;
rebuild source-only skin gain. Suit/hair/burgundy grade and anatomy ruler unchanged.
Old build/frames/manifest/registration/review/evidence and fixture archived under
review-before-face-v2; dated runtime-evidence.json remains historical.
Fit six exact35x38 selected East helmets at native scale1 by crown/axis against
idle authority. Bounded head-only erase removes bare hair; approved body is exact
outside head/component region and opaque canonical hardware pixels are exact.
Paired256/p128,224/H148,540ms loop/.168cell stride. Both manifests selected at
end of normal Bill loader; ACTIVE_ASSETS records literal paired paths.
21 bare package +25 helmet package checks;70 paired candidate-player and73
normal-loader checks pass. Normal fixture injects no candidate manifests: exact
bare/equipped source pixels, clocks, movement-distance phase, stationary hold,
wrap, grid selection/status and density tested. Native1792x1024 master/phase
board reviewed at148/82. Browser equipment selector loads both sequences.
NPC still walks through current controller; do not activate dormant old run
chooser to manufacture reachability. This is selected source/player proof, not
actual running route/save proof or owner visual acceptance. Lean joins, flight,
near/far limb layering, counter-swing and full-set motion polish remain open.
'''+f'''Candidate {reports['candidate']['seconds']}s; normal {reports['normal']['seconds']}s.
Both engine0/clean/fresh capture, scratch APPDATA. Strict guards failed:
candidate{reports['candidate']['realProfileChanges']}, normal{reports['normal']['realProfileChanges']},
{reports['normal']['realProfileFileCount']:,} real non-log files each. Attribution
unproven; no owner restore or repeated tests merely for a clean guard.
Full goal active. Next independently author West/North/South run with those
selected masters, then diagonal walk and cross-animation identity/material/
perspective/proportion/cadence polish. No commit/export, concurrent work preserved.
Lesson: skin calibration must exclude beard, hair and dark outlines. Hardware
fitting and a normal-loader gate are separate from biomechanical motion and
real-controller reachability; preserve each evidence scope.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill paired East run v2

## Objective and acceptance
Full Bill animation coverage matching masters, followed by cross-animation consistency/polish.

## Accepted decisions and constraints
Fixed anatomy rulers, exact native shared helmet, material-specific grade; preserve NPC behavior/profile/concurrent work. Reversible work authorized.

## Current state
Face-only source-grade correction, six helmet exports/manifest/registration/verification, paired preview. Normal loader and ACTIVE_ASSETS paired East run selection. New normal-loader fixture+UID/runner; expanded paired candidate fixture. Prior evidence retained separately.

## Verification
'''+summary+'''
## Next action
Independent West/North/South run sources, native shared helmet fits and normal-loader proof; then diagonal and whole-set polish. Full goal active.
'''
(P/'SELECTED_HANDOFF_v2.md').write_text(handoff,encoding='utf-8')
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
for folder in ['bill-run-east-candidate-native-v1','bill-run-east-selected-native-v2']:
 out=R/'output'/folder;files += [out/n for n in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png']]
for n in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json','tests/test_bill_run_east_candidate.gd','tests/test_bill_run_east_candidate.gd.uid','tests/test_bill_run_east_selected.gd','tests/test_bill_run_east_selected.gd.uid','tools/run_bill_run_east_selected_validation.py']:files.append(R/n)
(P/'selected-evidence-v2.json').write_text(json.dumps({'normalSelected':True,'normalNativeChecks':73,'pairedCandidateChecks':70,'packageChecks':46,'strictGuards':reports,'normalRunningRouteProven':False,'currentFileSha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill paired East run selected — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-run-east-coherent-v1/SELECTED_HANDOFF_v2.md.\n'
for n in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/n).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded paired East selection:46 package/73 normal +70 candidate checks, failed guards retained')
