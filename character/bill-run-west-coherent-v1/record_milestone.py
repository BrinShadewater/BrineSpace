from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
assert not (P/'runtime-evidence.json').exists(),'Preserve dated evidence'
out=R/'output/bill-run-west-selected-native-v1';report=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text()
assert report['returnCode']==0 and '73 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot']
b=json.loads((P/'verification.json').read_text());h=json.loads((P/'helmet-verification.json').read_text());assert b['passed'] and b['checks']==21 and h['passed'] and h['checks']==25
summary='''Bill paired West run selected — October 1, 2026.
Previous goal turn made substantive progress: corrected East skin authority,
fitted native helmet and selected paired East run with73 normal-loader checks.
West independently authored6pose source exec-e47f5c03-fbe7-484b-819d-1f1e87650cc5
uses selected WEST idle authority, no East mirror or transferred body pixels.
Exact prompt/source retained. One148/430 anatomical ruler across all six poses,
explicit pelvis X and source row baselines489/961, no per-pose stretch or extent
equalization. Pooled graphite quantile curve and local skin/hair/burgundy gains
reference WEST idle; skin authority excludes dark beard with luminance>65.
Six distinct running poses include changed arm silhouettes and opposite half
stride intent. Visible pose variation is not full biomechanical acceptance.
Native35x38 WEST canonical helmet, crown/axis registered with bounded head-only
erase; exact body pixels outside component/erase and opaque hardware verified.
Paired256/p128,224/H148,540ms loop, explicitrun-west .168cell stride. Normal
loader at end of Bill block and ACTIVE_ASSETS select paired whole-path manifests.
21 bare +25 helmet packaging checks,73 normal-loader native checks pass: no
candidate injection, exact pixels/density, timed and movement-distance phases,
wrap/stationary hold, selected statuses and grid selection. Fresh1792x1024
native148/82 board reviewed and browser equipment comparison loads both runs.
Normal Bill NPC still walks; old dormant test-walker run chooser unchanged.
No actual running route/save reachability claim or owner visual acceptance.
West row-to-row bob/stance compression, limb-side layering/counter-swing and
East/West cadence/detail/perspective/lean joins remain full-set polish work.
Do not stretch compressed frames to standing height to hide that review.
'''+f'''Native {report['seconds']}s engine0/clean/fresh capture, scratch APPDATA.
Strict overall passed=False: owner guard changed {report['realProfileChanges']}
among {report['realProfileFileCount']:,} non-log files. Attribution unproven;
retain failed result, no owner restore or retry merely for a clean interval.
PNG LFS filter confirmed. No commit/export; concurrent files preserved.
Full goal active. Next independently author North/South runs against their
own masters, then diagonal walk and full-set identity/material/anatomy/motion
consistency. Lesson: independently author directional gait to preserve camera
and asymmetric gear. Register source baselines and anatomy rulers explicitly;
compare compressed poses visually without per-pose size normalization.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill paired West run

## Objective and acceptance
Full master-consistent Bill animation set, then cross-animation consistency and polish.

## Accepted decisions and constraints
Direction-specific masters, fixed anatomical scale, native shared helmet, material-specific grade; preserve gameplay/profile/concurrent work. Reversible work authorized.

## Current state
New bill-run-west-coherent-v1 source/prompt,12 exports, paired manifests/build/registration, preview/verifiers. Normal loader/ACTIVE_ASSETS paired run selection; native fixture with UID and scratch runner.

## Verification
'''+summary+'''
## Next action
North and South independent run sources/native helmet fitting and normal-loader validation; diagonal walk and whole-set polish afterward. Goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
files += [out/n for n in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png']]
files += [R/n for n in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json','tests/test_bill_run_west_selected.gd','tests/test_bill_run_west_selected.gd.uid','tools/run_bill_run_west_selected_validation.py']]
(P/'runtime-evidence.json').write_text(json.dumps({'normalSelected':True,'normalNativeChecks':73,'packageChecks':46,'strictGuard':report,'normalRunningRouteProven':False,'currentFileSha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill paired West run selected — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-run-west-coherent-v1/HANDOFF.md.\n'
for n in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/n).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded paired West run:46 package/73 native checks, strict guard failure retained')
