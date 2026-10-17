from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];G=P.parent/'bill-rest-helmet-west-coherent-v1'
assert not (P/'candidate-evidence.json').exists() and not (G/'candidate-evidence.json').exists(),'Record later revisions separately'
reports=[]
for kind,n in [('west',109),('helmet-west',110)]:
    o=R/f'output/bill-rest-{kind}-candidate-native-v1';report=json.loads((o/'validation.json').read_text());log=(o/'native.log').read_text()
    assert report['returnCode']==0 and f'{n} checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and report['nativeScreenshot']
    reports.append(report)
assert json.loads((P/'verification.json').read_text())['passed'] and json.loads((G/'verification.json').read_text())['passed']
summary='''Bill paired west generic rest candidates — October 1, 2026.
Bare and shared helmet each3states/8 entry poses800ms, exact reversed wake800ms,
two closed-eye sleeping poses1200ms. Exact selected bare/equipped west idle,
256px/p128,224/H148, linear precomposed. New rest source
exec-36d899f3-d63d-41a3-acea-dfe64d0e7634 and lowering source
exec-0b7db075-2467-454c-947b-5a9148d4703a; initial generation
exec-65530fef-1e27-42bc-af11-6a237d6ff68f followed the east choreography and
is retained rejected. Corrected generation references only the west master,
nose left upright/head right and boots left supine, authored asymmetric gear.
Global master-referenced neutral/hair/face/bounded burgundy grading preserves
seams and scuffed hardware. One fixed main ruler[.31,148/446], lowering
[.18,148/710]; initial .28 horizontal ruler compressed reclining body length.
Native comparison led to .31 across the entire primary atlas, no per-pose scale.
Original check intervals retained; both paired versions rebuilt/revalidated.
Helmet is exact native selected west canonical, neck anchor[16,29], authored
body necks and side tilts5,5,5,15,40,90,90. Closed eye samples existing authored
front-left eyelid donor exec-0b1ad8c7-6822-4afb-816d-f4980cb3c9fe into9 RGB
pixels only, with shell/collar/face-outline and alpha exact outside the patch.
Both sleeping frames hold identical closed helmet placement. Initial warm-only
bare-head mask left a neutral dark hair tuft in forearm recline; bounded whole
head-alpha removal corrects it. Body pixels outside declared fitted area exact.
9 bare package invariants,30 equipment package checks and219 native player
checks (109bare/110helmet) pass. Native148/82 static boards reviewed against
each selected idle; reclining joins, arm/build/details, fine helmet/neck angle
and live cadence remain full-set polish items. No physical west bed, route,
interruption, Continue or normal selection proof. Selected specialized east
bunk unchanged. All four generic directions now have paired source candidates;
family compatibility/integration and whole-set consistency remain next.
'''+f'''Both scratch APPDATA native engines exit0, {reports[0]['seconds']}s bare and
{reports[1]['seconds']}s equipped. Both strict owner-profile guards FAILED:
bare{reports[0]['realProfileChanges']}, equipped{reports[1]['realProfileChanges']},
{reports[0]['realProfileFileCount']:,} non-log files each. Attribution unproven;
no owner restore or retry seeking clean guard. Prior intervals archived, repeat
validation justified by art ruler change. No commit/export, full goal active.
Lesson: a strong pose-sheet reference can override an explicit new facing;
remove the conflicting facing reference and regenerate authored anatomy. A
warm-color mask cannot remove neutral dark hair: inspect silhouette residuals
and use bounded head alpha removal while checking unchanged surrounding body.
Compare horizontal anatomical length as well as standing height; one shared
atlas ruler correction is preferable to bounding-box normalization per frame.
'''
for pack,kind,n,pkg in [(P,'west',109,9),(G,'helmet-west',110,30)]:
    handoff='# Project handoff\n\nUpdated: October 1, 2026 · Brine Space · Bill west paired rest\n\n## Objective and acceptance\nFull master-consistent Bill set followed by whole-set consistency and polish.\n\n## Accepted decisions and constraints\nExact idle, authored west anatomy, fixed rulers and matte grade; preserve owner profile and current east bunk.\n\n## Changed files\ncharacter/bill-rest-west-coherent-v1 and character/bill-rest-helmet-west-coherent-v1 source/prompts, builders, manifests/frames, preview and package verification; paired tests with UID and scratch runners. No production selection change.\n\n## Verification and remaining work\n'+summary+'\n## Next action\nPaired generic rest family compatibility/integration where appropriate, live motion/furniture evidence, remaining meals and full master/polish pass.\n'
    (pack/'HANDOFF.md').write_text(handoff,encoding='utf-8')
    o=R/f'output/bill-rest-{kind}-candidate-native-v1'
    files=[f for f in pack.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
    files.extend(o/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
    for archive in o.glob('interval-before-*'):files.extend(f for f in archive.iterdir() if f.is_file())
    stem=kind.replace('-','_')
    files.extend(R/name for name in [f'tests/test_bill_rest_{stem}_candidates.gd',f'tests/test_bill_rest_{stem}_candidates.gd.uid',f'tools/run_bill_rest_{stem}_candidate_validation.py'])
    (pack/'candidate-evidence.json').write_text(json.dumps({'nativeSubsystemPassed':True,'nativeChecks':n,'packageChecks':pkg,'strictGuard':json.loads((o/'validation.json').read_text()),'normalSelected':False,'visualScope':'static native148/82 board; live cadence/master/furniture acceptance pending','sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill paired west rest — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-rest-west-coherent-v1/HANDOFF.md.\n'
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded paired west rest:39 package/219 native checks; strict guard failures retained')
