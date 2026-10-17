from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[2]
summary='''Bill west eating/drinking candidates — October 1, 2026.
Independent built-in west sources: eating exec-8a937e79-25f1-406a-b3d4-d1b69b7336c8,
drinking exec-72c69b7d-af88-488c-bb02-67d3589de1f4. Raw PNGs/exact prompts retained.
Six whole poses per loop, seven 960ms slots with exact first-pose closure.
Selected west idle owns identity/matte neutral/face/hair/burgundy grading.
Fixed atlas rulers eating[.28,.329]/drinking[.29,.3395], sole223/master front boot;
256plane/pivot128,224/H148. No mirrored sources or per-pose scale normalization.
23 eating/24 drinking package checks PASS;64 native eating PASS11.56s and71 native
drinking PASS12.49s. Scratch APPDATA/all2,914 owner non-log files unchanged.
148/82 native boards and cross-action idle/eat/drink review inspected. Crown idle76,
eat76,drink76–77. Frame0 head alpha span idle116–142,eat115–140,drink115–138;
boots idle106–145,eat109–142,drink108–142. Fine harness/suit/boot silhouette,
hair and head profile differences remain for full-set polish. Technical passes
do not certify owner acceptance, physical service contact or saved phase behavior.
Lesson: compare opaque crown-to-sole against the selected master, not only the
148px standingHeight metadata; a shared ruler can still make an entire atlas tall.
Directional verifier literals must be updated alongside builders/fixtures.
Next west bowl/cup pickup and exact reverse returns/full family, then remaining
meal contact/saved phases/interrupt/Continue,rest/drydeath/wider inspection/full
cross-animation polish. Sources remain staged; full goal active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · BrineSpace · Bill west meal loops

## Objective and acceptance
Complete the full master-consistent Bill set, then cross-animation polish.
This milestone delivers two staged west loops, not the complete meal family.

## Accepted decisions and constraints
Use selected west idle identity, subdued matte materials and planted stance.
Independent directional art; fixed atlas rulers; source/prompt preservation.
Existing reversible animation work authorized. No runtime or geometry changes.

## Current state
'''+summary+'''
## Verification
Source/package bindings and native loaded pixels, metadata, pacing and closure pass.
Native sizes and cross-action master comparisons reviewed; fine design drift remains.
Native fixtures use scratch profiles and preserve every owner non-log file.

## Next action
Author west bowl pickup/return and cup pickup/return with exact selected idle and
new held-loop donor endpoints. Assemble all six west states and verify joins.
Keep north contact uncertainty and pending saved runtime phases explicit.
'''
for action,name,checks,native in [('eat','bill-meal-west-coherent-v1',23,64),('drink','bill-drink-west-coherent-v1',24,71)]:
    p=ROOT/'character'/name;out=ROOT/'output'/name.replace('-coherent','-candidate-native')
    # Output folders follow the maintained runner names, not the source folder name.
    out=ROOT/'output'/('bill-meal-west-candidate-native-v1' if action=='eat' else 'bill-drink-west-candidate-native-v1')
    report=json.loads((out/'validation.json').read_text());assert report['passed'] and not report['realProfileChanges']
    verify=json.loads((p/'verification.json').read_text());assert verify['passed']
    (p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
    paths=[f for f in p.iterdir() if f.is_file() and f.name!='candidate-evidence.json']+list((p/'sources').glob('*'))+list((p/'frames'/f'{action}-west').glob('*.png'))+[out/'validation.json',out/'loaded-water-carry.png',ROOT/f'tests/test_bill_{"meal" if action=="eat" else "drink"}_west_candidates.gd',ROOT/f'tools/run_bill_{"meal" if action=="eat" else "drink"}_west_candidate_validation.py']
    evidence={'status':'staged_candidate','checks':{'package':checks,'native':native},'native':report,'scope':'independent west loop source/native loading/master cross-review; full meal transitions and actual saved service pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in paths if f.is_file()}}
    (p/'candidate-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
heading='## Bill west eating/drinking candidates — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/relative).open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
with f.open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-drink-west-coherent-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded west meal loop sources, fresh evidence and remaining full-set scope')
