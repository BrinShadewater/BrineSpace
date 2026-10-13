"""Prepare a second whole stride pilot at identical physical reference density."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';D=P/'stride-000-v1';D.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
target=R/'character/bill-walk-east-material-v1/frames/bare/walk-east/000.png';Image.open(target).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(D/'edit-target.png')
refs=[dict(source=str(target),sourceSha256=sha(target),path=str(D/'edit-target.png'),sha256=sha(D/'edit-target.png'),role='only edit target: exact stride0/canvas')]
for name,role in [('original-master.png','original master identity/material authority; not a stride'),('detailed-donor.png','detailed idle/reach style continuity support; not a stride')]:
 shutil.copyfile(P/name,D/name);refs.append(dict(source=str(P/name),sourceSha256=sha(P/name),path=str(D/name),sha256=sha(D/name),role=role))
prompt='''Edit image1, the exact complete walking stride0 figure. Preserve its original stride, arm swing, foot positions, height, width, head size, natural connected anatomy, camera and transparent canvas placement. Image2 is the original Bill master identity/material authority. Image3 is our detailed idle/reach rendering continuity support only, not a pose to copy. Restore the master's warm angular face and brown hair, fine matte charcoal quilt stitching, restrained worn metal and exact square/ring insignia. Preserve all equipment positions. Keep the crown and sole positions exactly as in image1 and do not make his head or body bigger or brighter. One complete transparent walking figure; only material/design fidelity improves.'''
(D/'prompt.txt').write_text(prompt,encoding='utf-8');(D/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8');print('Prepared stride0 target and two matched-density support references.')
