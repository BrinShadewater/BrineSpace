"""Prepare exact selected East torch poses against current Bill master."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-torch-master-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((R/'character/bill-east-interact-master-consistency-v1/native/corrected-source-audit.json').read_text())['selected']['bare']['weld-east']
idle=R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png';master=R/'character/bill-east-walk-master-pilot-v1/original-master.png'
ref=Image.new('RGBA',(256,256));ref.alpha_composite(Image.open(idle).convert('RGBA'),(36,52));ref.resize((1024,1024),Image.Resampling.NEAREST).save(D/'idle-reference.png')
for slot,src in enumerate(s['files']):
 P=D/f'pose-{slot:03}';P.mkdir();target=R/src;Image.open(target).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(P/'edit-target.png')
 refs=[dict(path=str(p),sha256=sha(p),source=str(o),sourceSha256=sha(o),role=role) for p,o,role in [(P/'edit-target.png',target,'Exact selected torch pose, tool grip and flame direction'),(D/'idle-reference.png',idle,'Current master matte suit construction and warm face'),(master,master,'Original Bill identity')]]
 prompt=f'''Edit image1 into one complete East-facing Bill using his small hand-held blowtorch, existing action phase {slot} of6. Keep EXACT image1 body pose, build, height, placement, foot contacts, limb lengths/order, tool angle, grip, nozzle and small flame position. Image2 is current matching idle; image3 is original identity. Restore their matte charcoal quilted padded suit with fine diamond stitching, worn seams, straps, muted red upper-arm insignia and chest patch, subdued silver cuffs/kneepads/boot hardware. Warm readable angular brown-haired bearded face, medium brown hair, matching master midtones. No shiny bright suit, black flattened fabric or new light cast over the body. Shoulder patch belongs to the near upper-arm sleeve: one anatomical chain from shoulder to elbow to cuff to glove gripping torch. Far hand supports torch naturally at same selected grip. Exactly two connected arms, no spare waist hand, no chest-grown sleeve or disconnected elbow. Keep collar, head and shoulders attached. Preserve tiny blue-white core and orange tip flame aimed EAST/right, with same size/position and transparent pixels around it. One coherent whole figure, not pasted anatomy. Common1024square pivot(512,896), standingheight592; preserve exact image1 placement. True transparent RGBA; no background, ground shadow, halo, checkerboard, extra equipment, text or sprite sheet. Change only identity/material/detail consistency; retain tool and subtle original action motion.'''
 (P/'prompt.txt').write_text(prompt,encoding='utf-8');(P/'references.json').write_text(json.dumps(refs,indent=2)+'\n')
(D/'selected-contract.json').write_text(json.dumps(s,indent=2)+'\n');(D/'protected-inputs.json').write_text(json.dumps({p:sha(R/p) for p in [s['manifest']]+s['files']},indent=2)+'\n')
print('Six whole torch targets; exact selected tool/grip/flame geometry and timing retained.')
