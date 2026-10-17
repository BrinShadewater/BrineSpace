from pathlib import Path
from PIL import Image
import json,hashlib,sys
p=Path(__file__).resolve().parent;r=p.parents[1];phase=int(sys.argv[1]);version=int(sys.argv[2]);out=p/f'thigh-construction-phase{phase}-v{version}';out.mkdir(exist_ok=True)
row=json.loads((p/'material-repair-progress.json').read_bytes())['states'][phase];base=r/Path(row['candidateSources']['bare']['file']).parent;master=r/'character/branforth-west-direct-v2/master-input.png';box=(104,136,144,176)
for role,f,crop in [('edit-target',base/'bare-head-protected.png',box),('master-quilt-reference',master,(552,640,598,738))]:
 im=Image.open(f).convert('RGBA').crop(crop);im.resize((1024,1024),Image.Resampling.NEAREST if role=='edit-target' else Image.Resampling.LANCZOS).save(out/f'{role}.png')
prompt=(p/'thigh-construction-phase0-v244/prompt.txt').read_text(encoding='utf-8').replace('phase0',f'phase{phase}')
prompt+='\nColour continuity: keep Image1 original dark charcoal midtone brightness. Quilting is fine surface stitching, not bright padded ridges. Yellow seam is narrow, muted and follows this exact leg surface; do not brighten the cloth or introduce a straight seam unrelated to the limb. Preserve each leg independently and all original overlap; do not copy another pose.'
(out/'prompt.txt').write_text(prompt,encoding='utf-8');sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();files=[base/'bare-head-protected.png',base/'helmet-head-protected.png',master];refs=[out/'edit-target.png',out/'master-quilt-reference.png']
(out/'inputs.json').write_text(json.dumps(dict(phase=phase,baseFolder=base.relative_to(r).as_posix(),cropBox=box,admissionRectangle=[112,145,141,164],sourceSha256={f.relative_to(r).as_posix():sha(f) for f in files},referenceSha256={f.relative_to(r).as_posix():sha(f) for f in refs},promptSha256=sha(out/'prompt.txt'),normalChanged=False),indent=2)+'\n',encoding='utf-8')
print(f'Prepared thigh construction phase{phase}, version{version}.')
