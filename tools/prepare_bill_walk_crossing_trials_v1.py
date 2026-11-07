"""Prepare two representative crossing poses, preserving full target geometry."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for slot in [12,36]:
 D=P/f'stride-{slot:03}-v1';D.mkdir(exist_ok=False);target=R/f'character/bill-walk-east-material-v1/frames/bare/walk-east/{slot:03}.png';Image.open(target).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(D/'edit-target.png')
 refs=[dict(source=str(target),sourceSha256=sha(target),path=str(D/'edit-target.png'),sha256=sha(D/'edit-target.png'),role=f'only edit target: exact stride{slot}/canvas')]
 for name,role in [('original-master.png','original master identity/material authority; not a stride'),('detailed-donor.png','detailed idle/reach style continuity support; not a stride')]:
  shutil.copyfile(P/name,D/name);refs.append(dict(source=str(P/name),sourceSha256=sha(P/name),path=str(D/name),sha256=sha(D/name),role=role))
 prompt=f'''Edit image1, the exact complete walking stride{slot} figure. Preserve its original crossing stride, arm swing, foot positions, height, width, head size, natural connected anatomy, camera and transparent canvas placement. Image2 is the original Bill master identity/material authority. Image3 is detailed idle/reach rendering continuity support only, not a pose to copy. Restore the master's warm angular face and brown hair, fine matte charcoal quilt stitching, restrained worn metal and exact square/ring insignia. Preserve all equipment positions. Keep crown and sole positions exactly as image1; do not enlarge his head/body or raise his neck. One complete transparent walking figure; only material/design fidelity improves.'''
 (D/'prompt.txt').write_text(prompt,encoding='utf-8');(D/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
print('Prepared exact crossing12/36 targets with matched-density master/continuity references.')
