"""Prepare15 unique whole cargo poses; shared endpoints remain single sources."""
from pathlib import Path
from PIL import Image
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-cargo-handoffs-master-v1';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=R/'character/bill-cargo-east-master-head-v1/manifest.json';m=json.loads(old.read_text());idle=R/'character/bill-east-idle-master-motion-v1/frames/idle-east/000.png';carry=R/'character/bill-east-carry-master-v1/frames/000.png';master=R/'character/bill-east-walk-master-pilot-v1/original-master.png'
canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(Image.open(idle).convert('RGBA'),(36,52));canvas.resize((1024,1024),Image.Resampling.NEAREST).save(D/'idle-reference.png')
Image.open(carry).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(D/'carry-reference.png')
protected={p.relative_to(R).as_posix():sha(p) for p in [old,idle,carry,master]};states={};seen={};poses=[]
for action in ['pickup-east','unload-east']:
 state=next(s for s in m['states'] if s['id']==action);files=[];mapping=[]
 for slot,name in enumerate(state['frameFiles']):
  src=R/name.replace('res://','');files.append(src.relative_to(R).as_posix());h=sha(src);protected[files[-1]]=h
  if h in seen:mapping.append(seen[h]);continue
  identifier=f'{action}/pose-{slot:03}';seen[h]=identifier;mapping.append(identifier);poses.append(identifier);P=D/identifier;P.mkdir(parents=True)
  Image.open(src).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(P/'edit-target.png')
  refs=[dict(path=str(p),sha256=sha(p),source=str(o),sourceSha256=sha(o),role=role) for p,o,role in [(P/'edit-target.png',src,'Exact selected cargo pose: crate/hand/feet geometry'),(D/'idle-reference.png',idle,'Current matte idle detail and warm face'),(D/'carry-reference.png',carry,'Current carry material and cargo design; not its walking pose'),(master,master,'Original Bill identity')]]
  prompt=f'''Edit image1 into one complete East-facing Bill {action} phase{slot}. Preserve image1 EXACT whole pose, crouch/bend depth, standing size, slim body build, head angle, collar/shoulders, two actual limbs, feet and floor contact. Preserve its EXACT cargo crate silhouette, size, angle, perspective, latch, handles and location, and exact glove contact, grip/occlusion. Ground crate stays on floor if source grounded; carried crate stays touching both original grip locations. Do NOT substitute the walking pose or foot-out stance of reference3. Images2/3/4 supply identity and material only. Restore their detailed matte charcoal diamond-quilted padded suit, subtle worn stitches/seams, harness/belt/pouches, muted red shoulder/chest markings, subdued silver metal, warm readable bearded angular face and medium brown hair. Near shoulder patch sits on real sleeve continuous shoulder-to-elbow-to-cuff-to-glove, no chest-grown arm or extra hand. No extra crate, detached prop, altered case design, shiny bright fabric, crushed dark face or uniformly flat black suit. Keep body attached through collar/shoulders. One complete figure plus original crate, no part stamping. All references1024square common pivot512,896 and standingH592; crouching must naturally lower head, do not stretch bent poses to standing height. Keep image1 placement and planted feet. Transparent RGBA, no background/shadow/halo/text/sheet/checkerboard. Only coherent identity/material/detail restoration preserving motion and cargo handling.'''
  (P/'prompt.txt').write_text(prompt);(P/'references.json').write_text(json.dumps(refs,indent=2)+'\n')
 states[action]=dict(state=state,files=files,poseMapping=mapping)
(D/'selected-contract.json').write_text(json.dumps(dict(manifest=old.relative_to(R).as_posix(),states=states,uniquePoses=poses),indent=2)+'\n');(D/'protected-inputs.json').write_text(json.dumps(protected,indent=2)+'\n')
print(json.dumps(dict(uniqueWholeTargets=len(poses),sourceSlots=17,exactOldAliases=2,protected=len(protected))))
