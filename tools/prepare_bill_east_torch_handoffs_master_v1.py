"""Prepare eight whole-figure intermediate poses; inherit exact master endpoints."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-torch-handoffs-master-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'character/bill-torch-actions-v1/manifest.json';m=json.loads(old.read_text())
idle=R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png';torch=R/'character/bill-east-torch-master-v1/frames/000.png';master=R/'character/bill-east-walk-master-pilot-v1/original-master.png'
canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(Image.open(idle).convert('RGBA'),(36,52));canvas.save(D/'idle-endpoint.png');canvas.resize((1024,1024),Image.Resampling.NEAREST).save(D/'idle-reference.png')
Image.open(torch).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(D/'torch-reference.png')
protected={old.relative_to(R).as_posix():sha(old),idle.relative_to(R).as_posix():sha(idle),torch.relative_to(R).as_posix():sha(torch)};states={}
for action in ['torch-draw-east','torch-stow-east']:
 state=next(s for s in m['states'] if s['id']==action);files=[]
 for slot,name in enumerate(state['frameFiles']):
  src=old.parent/name;files.append(src.relative_to(R).as_posix());protected[files[-1]]=sha(src)
  if slot in [0,5]:continue
  P=D/action/f'pose-{slot:03}';P.mkdir(parents=True)
  Image.open(src).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(P/'edit-target.png')
  refs=[dict(path=str(p),sha256=sha(p),source=str(o),sourceSha256=sha(o),role=role) for p,o,role in [(P/'edit-target.png',src,'Exact selected tool handoff pose and arm/tool geometry'),(D/'idle-reference.png',idle,'Current idle matte detail and warm identity'),(D/'torch-reference.png',torch,'Matching active torch materials and grip'),(master,master,'Original Bill identity')]]
  prompt=f'''Edit image1 into one complete East-facing Bill in action {action}, intermediate phase{slot} of6. Preserve image1 EXACT pose, standing size, body build, feet, limb lengths, near/far arm order, head/collar position, wrist angles and torch presence/absence/location. Images2/3/4 are identity/material references, NOT replacement poses. Restore their matte charcoal quilted padded suit, fine diamond stitches, worn seams, harness/belt/pouches, muted red shoulder/chest markings and subdued silver hardware. Warm readable angular bearded face, medium brown hair. The near shoulder patch is ON a continuous upper-arm sleeve connecting actual shoulder to elbow to cuff to glove. Two actual attached arms only, no chest-grown spare sleeve, extra waist hand or detached shoulder. Preserve exact selected grasp and tool angle; far hand naturally occluded. Keep torch unlit in these intermediate phases, or absent if absent in image1; do not invent flame or equipment. {('He is drawing the torch from his belt and bringing it forward.' if action=='torch-draw-east' else 'He is lowering and returning the torch to his belt.')} No glossy bright suit, near-black flat fabric, lighting change, enlarged bicep or floating tool. One coherent complete figure with body connected through collar and shoulders. All1024square references use pivot(512,896), H592; preserve exact image1 placement/contact. Transparent RGBA, no background/shadow/halo/checkerboard/text/sheet. Only identity/material/detail repair while retaining handoff motion and planted feet.'''
  (P/'prompt.txt').write_text(prompt,encoding='utf-8');(P/'references.json').write_text(json.dumps(refs,indent=2)+'\n')
 states[action]=dict(state=state,files=files)
(D/'selected-contract.json').write_text(json.dumps(dict(manifest=old.relative_to(R).as_posix(),states=states),indent=2)+'\n')
(D/'protected-inputs.json').write_text(json.dumps(protected,indent=2)+'\n')
print('Eight intermediate targets; four exact idle/active-torch endpoint aliases planned.')
