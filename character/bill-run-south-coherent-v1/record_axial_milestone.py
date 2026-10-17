from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];N=P.parent/'bill-run-north-coherent-v1'
assert not (P/'runtime-evidence.json').exists() and not (N/'runtime-evidence.json').exists(),'Preserve dated evidence'
reports={}
for direction,folder in [('north',N),('south',P)]:
 out=R/f'output/bill-run-{direction}-selected-native-v1';report=json.loads((out/'validation.json').read_text());log=(out/'native.log').read_text()
 assert report['returnCode']==0 and '73 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot']
 b=json.loads((folder/'verification.json').read_text());h=json.loads((folder/'helmet-verification.json').read_text());assert b['passed'] and b['checks']==21 and h['passed'] and h['checks']==25;reports[direction]=report
summary='''Bill paired North/South run selected — October 1, 2026.
Previous goal turn made substantive progress: paired West run independently
authored/selected, with46 packaging/73 native checks and recorded lessons.
North independent rear source exec66b707d7-9f45-4b17-a7f6-2a1c41164e64 references
selected NORTH master: rear backpack/control inset/harness, brown hair/nape,
no face reveal, alternating rear heels/lifted soles. One148/480 ruler; explicit
pelvis axes/source baselines582/1164. Pooled graphite/hair/burgundy grade matches
rear master; no front-face calibration applied to rear hair. Native35x36 rear
helmet fitted by crown/axis, body exact outside bounded head/component region.
South v1 execa2d05bf2-647b-4c8c-88e3-c2f523fd1245 read too broad in chest/head.
Retained rejected source/prompt. Authored v2 exec0a83e3af-cabc-4088-9e0b-daeab7c3cd6e
narrows source anatomy against FRONT master while preserving camera/stride intent,
not per-frame horizontal squeezing. One148/430 ruler, source baselines502/982;
pooled graphite and local skin/hair/burgundy grades, beard excluded from skin
authority. Native36x42 front helmet; exact hardware/body-protection checks.
Both independent paired packs select12frames each,256/p128,224/H148 density,
6phase540ms loops, .168cell directional stride. Normal loader/ACTIVE_ASSETS use
whole literal paired manifest paths.21bare+25helmet checks each/92packaging;
73 normal-loader checks each/146native: no candidate injection, exact selected
pixels, density, timed and movement-distance clocks, wrap/stationary hold and
grid selection/status. Both fresh1792x1024 native148/82 boards reviewed;
North rear and South frontal equipped browser comparisons load all phases.
All four cardinal run profiles now use renewed independently authored bodies
and native directional shared helmets. This is source coverage, not final
motion/anatomy/material or owner acceptance. Flight, gait near/far side layering,
counter-swing, cross-direction bob and detailed suit/face/camera consistency,
idle/walk/run lean joins and whole-set polish remain open. Current Bill NPC
still walks; no activation of dormant test-walker chooser, actual run route/save
proof or changed speed claimed. Current source-only audit now212bare/193helmet
selected keys; originalbare walk-south-east remains, plus accepted specialized
East bunk. Equipment retained original eat/drink are inactive sealed-mouth
presentation; helmet meal uses inspection. Do not replace accepted bunk or
label inactive meals defective merely for source age. Audit dated run-v2
preserves old inventory and is not live reachability/quality proof.
'''+f'''North {reports['north']['seconds']}s, South {reports['south']['seconds']}s,
both engine0/clean/fresh captures under scratch APPDATA. Strict guards BOTH
failed: North{reports['north']['realProfileChanges']}, South{reports['south']['realProfileChanges']},
{reports['south']['realProfileFileCount']:,} real non-log files each. Attribution
unproven; failed results retained, no owner restore or retry for clean interval.
PNG LFS filter confirmed. No commit/export; concurrent work preserved.
Full goal active. Next inspect/renew remaining diagonal-walk coverage and
runtime facing consumers, then full-set master/detail/material/scale/proportion/
camera/motion consistency and wider physical/save contexts still unproven.
Lesson: rear running uses heels/soles and rear equipment, front running uses
foreshortened knees and front boot projection. Repair broad source anatomy by
authoring against its own master, then use one fixed anatomy ruler; don't
stretch individual compressed poses or transfer a frontal skin mask onto nape.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill paired axial runs

## Objective and acceptance
Full master-consistent Bill set, then cross-animation consistency and polish.

## Accepted decisions and constraints
Directional masters, fixed anatomical source rulers, native shared helmets and local material grade; preserve NPC behavior/profile/concurrent work. Reversible work authorized.

## Current state
New North/South paired run source packs,24exports total, manifests/builds/registration/previews/verifiers. South rejected v1 retained. Normal loader/ACTIVE_ASSETS select both. Native fixtures with UIDs/scratch runners, updated source-only audit run-v2.

## Verification
'''+summary+'''
## Next action
Diagonal source/facing review and renewal; full-set master identity/material/anatomy/perspective/cadence polish and remaining real contexts. Goal active.
'''
for folder in [N,P]:
 (folder/'HANDOFF.md').write_text(handoff,encoding='utf-8');files=[f for f in folder.rglob('*') if f.is_file() and '__pycache__' not in f.parts];direction='north' if folder==N else 'south';out=R/f'output/bill-run-{direction}-selected-native-v1'
 files += [out/n for n in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png']]
 files += [R/n for n in ['scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json',f'tests/test_bill_run_{direction}_selected.gd',f'tests/test_bill_run_{direction}_selected.gd.uid',f'tools/run_bill_run_{direction}_selected_validation.py','tools/audit_bill_selected_sources_2026_10_01_run_v2.py','character/bill-selected-source-audit-2026-10-01-run-v2/source-inventory.json']]
 (folder/'runtime-evidence.json').write_text(json.dumps({'normalSelected':True,'normalNativeChecks':73,'packageChecks':46,'strictGuard':reports[direction],'normalRunningRouteProven':False,'currentFileSha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill paired axial runs selected — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-run-south-coherent-v1/HANDOFF.md.\n'
for n in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/n).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded North/South paired selection:92 package/146 native checks, failed guards retained')
