from pathlib import Path
import hashlib,json,os,uuid,subprocess
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];name='walk00-case-v2'
inputs=json.loads((p/f'{name}-inputs.json').read_bytes())
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs['preCallSha256'].items())
base=np.array(Image.open(p/inputs['baseFile']).convert('RGBA'));out=np.array(Image.open(p/f'{name}.png').convert('RGBA'))
mask=np.ones(base.shape[:2],bool);mask[104:169,88:166]=False
assert mask.sum()==60466 and np.array_equal(base[mask],out[mask])
file=p/f'{name}-review.json';report=json.loads(file.read_bytes())
assert report['rawSha256']==hashlib.sha256((p/f'{name}-raw.png').read_bytes()).hexdigest()
report.update(visualReviewPending=False,sourceAcceptance=False,selected=False,
    disposition='provisional_case_height_improved_extra_yellow_fleck_requires_cleanup',
    generation='exec-e1424b90-300a-46e7-9545-ae39be906a22',
    findings=['Raw, full, detail and station comparisons inspected against fixed-scale standing master reference. Case larger/lower at waist, closer to master than originalphase0.',
    'Small yellow fleck above near glove persists alongside lower belt meter: possible reference contamination again. Cleanup/tool identity still required; lower meter may have changed within upper admission, no exact meter-preservation claim.',
    '60466outside exact; head above104 and legs below169 unchanged. Four-key study still points to earlier tool-fix0; newv2 not admitted to full gait or normal runtime.'])
file.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
rasters=[str(f.relative_to(r)).replace('\\','/') for f in p.glob(name+'*.png')]
attrs=subprocess.run(['git','check-attr','filter','--',*rasters],cwd=r,capture_output=True,text=True,check=True).stdout.splitlines()
assert len(attrs)==len(rasters) and all(s.endswith(': lfs') for s in attrs)
section='''### James West first carry-key case height revision — October 2, 2026

walk00-case-v2 generated from repaired0upper crop plus same-scale standing master
reference lowers/enlarges case toward master waist placement. Raw/full/detail/
station comparisons inspected;60466outside exact, frozen pre-call hashes stable,
raster LFS verified. Small yellow fleck above glove persists alongside lower belt
meter; provisional/unselected, sourceAcceptance false. Lower meter is within upper
admission and may change: do not claim this revision protects it exactly.
Original four-key study remains unchanged. No complete gait/native/normal binding.
Lesson: full master reference provides dimensions but can still contaminate tools;
combine master geometry with isolated case material and explicit original belt
protection, inspect final crop seams/tool ownership before motion expansion.
Next local yellow-fleck/tool cleanup, cross-key case geometry, complete coherent
paired walking cycle and actual joins/context/Continue. Full goal incomplete.
Review:character/james-west-carry-walk-keys-v1/walk00-case-v2-review.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James West carrying source keys and belt-tool review');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
handoff=p/'HANDOFF.md';text=handoff.read_text(encoding='utf-8')
text=text.replace('Correct phase0case/grip scale and height against standing master/other keys.','Phase0case-v2 lowers/enlarges case closer to master; raw/full/detail/station\nreviewed,60466outside/frozen inputs/LFS pass. Small yellow fleck above glove\nrequires cleanup; original four-key study unchanged. Correct tools then compare\ncase geometry across all keys before expansion.')
handoff.write_text(text,encoding='utf-8')
print('Case-height revision reviewed and protected pixels pass; yellow fleck remains provisional. Five guides/handoff updated; goal incomplete.')
