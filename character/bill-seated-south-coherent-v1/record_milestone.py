from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;H=P.parent/'bill-seated-helmet-south-coherent-v1'
note='''
Bill south sofa sitting base staged — September30,2026. Fourgear states/24refs:
bare/helmet sit-down and reversed rise,800ms,frozen ruler [.28,.3027],matte
current south idle grade,native selected helmet,exact standing entry/exit.
50package and179native candidate checks pass10.89sec;fresh native82 contact
reviewed;2,914 real non-logfiles unchanged. Runtime/registry south unchanged.
Observation sofa actually faces south; establish that seated base before authoring
reading. Crown lowers through forward hinge then rises9px when torso straightens
into rest; do not force crown monotonicity by height-normalizing the figure.
Actual sofa/hip/knee contact remains unproven. Next: south breathing/reading,
real sofa transitions,remaining directional life/rest/ground death and final polish.
Full goal active. Handoff: character/bill-seated-south-coherent-v1/FAMILY_HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south sofa sitting base staged — September30,2026\n'+note+'\n').encode('utf-8')+status.read_bytes())
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
files=[P/'sources/sit-v1.png',P/'sources/prompt-sit-v1.txt',P/'sources/master-reference.png',P/'build.py',P/'manifest.json',P/'registration.json',P/'verification.json',H/'build.py',H/'manifest.json',H/'helmet-registration.json',ROOT/'tests/test_bill_seated_south_candidates.gd',ROOT/'tools/run_bill_seated_south_candidate_validation.py']
native=ROOT/'output/bill-seated-south-candidate-native-v1'
data={'status':'staged_candidate','generation':'exec-b9d74194-8426-40ef-8bb2-bac3db9abc1b','prompt':'sources/prompt-sit-v1.txt','native':json.loads((native/'validation.json').read_text(encoding='utf-8')),'hashes':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'nativeScreenshotSha256':hashlib.sha256((native/'loaded-water-carry.png').read_bytes()).hexdigest(),'scope':'candidate sprite-plane/life clocks;actual sofa/reading/selection pending'}
(P/'candidate-evidence.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
(H/'FAMILY_HANDOFF.md').write_text('Paired candidate authority: ../bill-seated-south-coherent-v1/FAMILY_HANDOFF.md\n',encoding='utf-8');print('Recorded staged south sitting base and furniture-perspective lesson')
