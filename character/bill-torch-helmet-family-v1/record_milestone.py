from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
assert not (P/'runtime-evidence.json').exists(),'Preserve dated evidence'
out=R/'output/bill-torch-helmet-family-native-v1'
report=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text()
assert report['returnCode']==0 and '395 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot']
package=json.loads((P/'verification.json').read_text());assert package['passed'] and package['checks']==236
summary='''Bill helmet cardinal torch family selected — October 1, 2026.
New12 equipment clips/72 frames cover draw/weld/stow in four directions.
Normal grid loader and ACTIVE_ASSETS select literal paired equipment manifest
after approved bare torch family. Native canonical standing helmets from
selected seated equipment masters keep scale1, registered by bare crown/axis.
Bounded head erasure removes all RGB hair classes; body/tool/flame pixels
outside head/component region remain exact. Exact equipped idle endpoints,
draw/work/stow joins; matched520ms finite draw/stow and960ms weld loops.
Shared256/p128,224/H148 density.236 package checks and395 normal-loader native
checks pass, fresh1536x3072 rendered board reviewed. Browser comparison loads
all cardinal chains at148/82/54/27 actual display heights; East weld and South
standing reviewed. Static captures and sampled playback are not full cadence
or owner visual acceptance. South shoulder/body brightness versus selected
idle and broader master detail/material consistency remain full-set polish.
Construction explicitly excludes helmeted builders in reconcile/eligibility;
missing equipped weld was source coverage, not an observed gameplay disappearance.
No gameplay eligibility change or equipped construction/route/save claim.
'''+f'''Native engine0/clean, {report['seconds']}s scratch APPDATA. Strict overall
passed=False: real owner-profile guard changed {report['realProfileChanges']}
among {report['realProfileFileCount']:,} non-log files. Attribution unproven;
retain failed guard, no owner restore or rerun merely to get a clean interval.
PNG Git LFS filter confirmed. No commit/export; concurrent work preserved.
Next: inspect remaining original cardinal run and diagonal-walk sources and
real consumers, then full-set master proportions/detail/matte/cadence polish.
Lesson: separate equipment source availability from gameplay eligibility.
Reuse approved tool/body pixels and native selected hardware with bounded
registration, verifying joins and clocks separately from motion acceptance.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill helmet torch

## Objective and acceptance
Complete Bill master-consistent animation set, then full cross-animation polish.

## Accepted decisions and constraints
Native selected helmet, approved tool/body art, exact idle joins; preserve current construction eligibility, owner profile and concurrent work. Reversible work authorized.

## Current state
New character/bill-torch-helmet-family-v1 build, manifests,72 PNGs, registration/hashes, preview, verification and evidence. Normal equipment loader in scripts/grid_canvas.gd and ACTIVE_ASSETS override. Native fixture plus paired UID and scratch runner.

## Verification
'''+summary+'''
## Next action
Inspect original run/diagonal sources and consumers; then full-set master/material/anatomy/motion pass. Full goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[f for f in P.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
files += [out/n for n in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png']]
files += [R/n for n in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json','tests/test_bill_torch_helmet_family.gd','tests/test_bill_torch_helmet_family.gd.uid','tools/run_bill_torch_helmet_family_validation.py']]
(P/'runtime-evidence.json').write_text(json.dumps({'normalSelected':True,'nativeSubsystemPassed':True,'nativeChecks':395,'packageChecks':236,'strictGuard':report,'equippedConstructionProven':False,'currentFileSha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill helmet cardinal torch family — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-torch-helmet-family-v1/HANDOFF.md.\n'
for n in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/n).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded236 package/395 native checks; strict guard failure retained')
