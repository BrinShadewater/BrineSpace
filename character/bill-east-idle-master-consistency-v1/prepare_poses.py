from pathlib import Path
from PIL import Image
import json,hashlib,sys
P=Path(__file__).resolve().parent;R=P.parent.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();a=json.loads((P/'source-baseline.json').read_text());base=json.loads((P/'job-000.json').read_text());prompt=Path(base['promptFile']).read_text()
for slot in map(int,sys.argv[1:]):
 jobPath=P/f'job-{slot:03}.json';assert not jobPath.exists();source=R/a['rows'][slot]['path'];assert sha(source)==a['rows'][slot]['sha256'];canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(Image.open(source).convert('RGBA'),(68,52));target=P/f'sources/target-{slot:03}.png';canvas.resize((1408,1408),Image.Resampling.NEAREST).save(target);pf=P/f'sources/prompt-{slot:03}.txt';pf.write_text(prompt.replace('pose 0 of','pose '+str(slot)+' of'),encoding='utf-8');refs=[dict(x) for x in base['references']];refs[0].update(path=str(target),sha256=sha(target));job={**base,'status':'prepared','slot':slot,'source':str(source),'sourceSha256':sha(source),'references':refs,'promptFile':str(pf),'promptSha256':sha(pf),'submittedPromptSha256':sha(pf)}
 for key in ['originalPath','savedPath','sha256','generationId']:job.pop(key,None)
 jobPath.write_text(json.dumps(job,indent=2)+'\n')
print('Neighbor targets and exact phase-specific prompts bound.')
