"""Freeze whole compression correction at unchanged anatomical scale."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-south-run-material-v1/sources'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
req=json.loads((BASE/'passing-05.request.json').read_text());prompt=(BASE/'passing-05.prompt.txt').read_text().strip()
prompt=prompt.replace('Reference3 original master','Reference3 is the previous two-figure passing source, ONLY a leg-side guide: preserve its correct viewer-RIGHT supporting boot and lifted viewer-LEFT foot, but correct its nearly straight supporting knee and level head. Its wider torso must not become anatomical authority. Reference4 original master')
prompt+='''

COMPRESSION CORRECTION: figure1 is visibly LOWER than figure2 while both planted foot soles stay on the SAME floor baseline. Figure1 supporting viewer-RIGHT knee bends enough to lower the pelvis, torso and head by about5% of the neutral standing height. This lowering comes from NATURAL KNEE/HIP FLEXION at unchanged adult anatomy scale, never shrinking the head/torso or stretching the legs. Figure1 head must therefore sit noticeably BELOW neutral head, and its shoulders/waist lower correspondingly. The RIGHT foot remains planted, LEFT foot lifted beneath pelvis. Keep a modest running lean. Figure2 remains original neutral ruler. No halo, glow, coloured haze or shadows: transparency starts directly outside the complete figure silhouette. Entire complete bodies only.'''
path=BASE/'passing-06.prompt.txt';assert not path.exists();path.write_text(prompt+'\n',encoding='utf-8')
refs=[BASE/'selected-south-idle-gait.png',BASE/'right-support-selected-walk3.png',BASE/'passing-05.raw.png',ROOT/'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png']
for key in ['generationId','originalGeneratedPath','rawSha256']:req.pop(key,None)
req.update(status='frozen whole compression correction before generation',promptSha256=sha(path),orderedReferences=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in refs],priorDraft='passing05 correct support side but nearly level neutral head; source retained')
(BASE/'passing-06.request.json').write_text(json.dumps(req,indent=2)+'\n')
print('Frozen06 complete compression correction with four ordered references.')
