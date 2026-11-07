"""Prepare complete fixed-canvas walk target and master/style references."""
from pathlib import Path
from PIL import Image
import hashlib,json
R=Path(__file__).resolve().parents[1];P=R/'character/bill-east-walk-master-pilot-v1';P.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
refs=[(R/'character/bill-walk-east-material-v1/frames/bare/walk-east/024.png','edit-target.png','only edit target; exact current whole stride pose/canvas'),(R/'character/bill-east-idle-interact-joined-v1/head-consistency-pilot-v3/original-master.png','original-master.png','original master identity/material/camera authority only'),(R/'character/bill-east-reach-adjacent-motion-v1/sources/raw-001.png','detailed-donor.png','detailed matte face/quilt rendering continuity support only, not a pose')]
records=[]
for path,name,role in refs:
 im=Image.open(path).convert('RGBA');im=im.resize((1024,1024),Image.Resampling.NEAREST if name=='edit-target.png' else Image.Resampling.LANCZOS);im.save(P/name);records.append(dict(source=str(path),sourceSha256=sha(path),path=str(P/name),sha256=sha(P/name),role=role))
prompt='''Edit image1, the complete walking stride figure, on its exact existing transparent canvas. Preserve this exact stride pose, feet/boot contacts, limb lengths, body width, height, head size, camera and image placement. Image2 is the original Bill master design/material authority. Image3 is rendering continuity support from our improved idle/reach family only; do not borrow its pose. Bring the walking figure closer to the original master's warm angular face and brown hair, restrained matte quilted charcoal suit, fine worn stitching and metal, square/ring insignia and detailed belt fittings. Preserve the walking figure's equipment layout and natural connected anatomy. No brighter glossy finish, inflated body, giant head, new limbs or pose change. Return one complete transparent whole walking figure at the exact original size/placement; improve identity and material fidelity without changing the stride.'''
(P/'prompt.txt').write_text(prompt,encoding='utf-8');(P/'references.json').write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
print('Prepared three full1024square references; original walk target nearest4x, supporting refs whole uniform resize only.')
