"""Prepare exact original walking targets; never derive from a rejected edit."""
from pathlib import Path
import copy, hashlib, json, sys
from PIL import Image
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
template=json.loads((OUT/'generation-job-bare-walk-003-v1.json').read_text(encoding='utf-8'))
assessment=ROOT/'character/bill-walk-west-master-repair-v2/bank-assessment.json'
poses={p['frame']:p for p in json.loads(assessment.read_text(encoding='utf-8'))['poses']}
prompt=Path(template['promptFile']).read_text(encoding='utf-8')
for frame in map(int,sys.argv[1:]):
 key=f'bare-walk-{frame:03}'
 job=OUT/f'generation-job-{key}-v1.json'
 assert not job.exists(),job
 src=assessment.parent/poses[frame]['study']
 im=Image.open(src).convert('RGBA');assert im.size==(256,256)
 target=OUT/'sources'/f'{key}-target-4x.png'
 canvas=Image.new('RGBA',(352,352));canvas.alpha_composite(im,(32,0))
 canvas.resize((1408,1408),Image.Resampling.NEAREST).save(target)
 pf=OUT/'sources'/f'{key}-prompt-v1.txt';pf.write_text(prompt,encoding='utf-8')
 q=copy.deepcopy(template)
 for name in ('originalPath','savedPath','sha256','generationId'):q.pop(name,None)
 q.update(key=key,status='prepared',sourcePath=str(src),sourceSha256=sha(src),
  references=[{'path':str(target),'sha256':sha(target),'role':'single edit target'}],
  promptFile=str(pf),promptSha256=sha(pf),submittedPromptSha256=sha(pf))
 job.write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
 print(key+' prepared from original source')
