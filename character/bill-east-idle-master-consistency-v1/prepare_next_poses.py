from pathlib import Path
from PIL import Image
import json,hashlib,shutil,sys
R=Path.cwd();P=R/'character/bill-east-idle-master-consistency-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();a=json.loads((P/'source-baseline.json').read_text())
H=P/'key-pose-evidence-v1';H.mkdir(exist_ok=False)
for name in ['review.json','validation.json','key-pose-review.png','density-review.png','build_review.py']:shutil.copy2(P/name,H/name)
(H/'candidate-frames').mkdir()
for n in [0,18,36]:shutil.copy2(P/f'candidate-frames/{n:03}.png',H/f'candidate-frames/{n:03}.png')
peak=Image.open(P/'sources/raw-036.png').convert('RGBA');peak.resize((1408,1408),Image.Resampling.LANCZOS).save(P/'sources/peak-reference.png')
base=json.loads((P/'job-018.json').read_text());inputs=base['frozenInputs'].copy()
for f in [P/'provenance-036.json',P/'sources/raw-036.png',P/'source-baseline.json']:inputs[str(f)]=sha(f)
for slot in [0,9,27]:
 source=R/a['rows'][slot]['path'];assert sha(source)==a['rows'][slot]['sha256'];canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(Image.open(source).convert('RGBA'),(68,52));target=P/f'sources/target-{slot:03}.png';canvas.resize((1408,1408),Image.Resampling.NEAREST).save(target)
 prompt=Path(base['promptFile']).read_text().replace('pose 18','pose '+str(slot)).replace('an already improved matching idle/interaction endpoint','the already improved peak-breathing pose').replace('endpoint, supporting','pose, supporting')+'\nKeep Image 1 exact crown, sole and foot coordinates; the body must not rise or sink. The soles remain planted at the original source contact. Small source breathing displacement only; reference3 supplies rendering consistency, never chest/limb shape or pose.'
 pf=P/f'sources/prompt-{slot:03}.txt';pf.write_text(prompt,encoding='utf-8');refs=[{'path':str(target),'role':'only edit target, exact original phase and placement'},{'path':str(P/'sources/original-east-master-common.png'),'role':'original master identity/material authority'},{'path':str(P/'sources/peak-reference.png'),'role':'peak pose rendering only, not phase or shape authority'}]
 for ref in refs:ref['sha256']=sha(Path(ref['path']))
 job={**base,'status':'prepared','slot':slot,'source':str(source),'sourceSha256':sha(source),'references':refs,'promptFile':str(pf),'promptSha256':sha(pf),'submittedPromptSha256':sha(pf),'frozenInputs':inputs}
 for key in ['originalPath','savedPath','sha256','generationId']:job.pop(key,None)
 (P/f'job-{slot:03}.json').write_text(json.dumps(job,indent=2)+'\n')
print('Prior reviewed milestone archived; source0/9/27 exact edit inputs prepared with peak rendering reference.')
