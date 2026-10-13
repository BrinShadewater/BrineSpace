"""Keep the historical bank; repair two complete backward-arm sources."""
from pathlib import Path
from PIL import Image
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];A=R/'character/bill-east-run-master-v1';D=R/'character/bill-east-run-master-v2';D.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['idle-reference.png','selected-contract.json','protected-inputs.json']:shutil.copy2(A/name,D/name)
inherited={}
for slot in range(6):
 S=D/f'pose-{slot:03}';S.mkdir();old=A/S.name
 if slot not in [0,5]:
  for name in ['raw.png','prompt.txt','references.json','receipt.json','edit-target.png']:shutil.copy2(old/name,S/name)
  inherited[str(slot)]={name:dict(path=str(old/name),sha256=sha(old/name)) for name in ['raw.png','prompt.txt','references.json','receipt.json']}
  continue
 Image.open(old/'raw.png').convert('RGBA').resize((1024,1024),Image.Resampling.LANCZOS).save(S/'edit-target.png')
 geometry=old/'edit-target.png';master=R/'character/bill-east-walk-master-pilot-v1/original-master.png'
 refs=[dict(path=str(p),sha256=sha(p),source=str(src),sourceSha256=sha(src),role=role) for p,src,role in [(S/'edit-target.png',old/'raw.png','Whole figure edit target with the reported defective backward arm'),(geometry,geometry,'Original same running phase geometry; reference for continuous arm silhouette'),(D/'idle-reference.png',A/'idle-reference.png','Current master matte detail and shoulder anatomy'),(master,master,'Original master identity')]]
 prompt=f'''Repair image1, one complete East-facing running Bill in phase{slot}. The backward-swinging camera-near arm looks disconnected from the red shoulder patch and merges into the chest. Correct that anatomy. The red patch belongs ON the camera-near upper-arm sleeve attached to the shoulder joint just below the collar. Trace ONE unbroken arm from that shoulder: upper arm slopes diagonally down/back toward image-left, a single elbow behind the flank, then forearm/cuff and gloved fist behind the body. Upper-arm sleeve, elbow, forearm and hand must form ONE visible continuous chain, with clear silhouette and realistic adult arm lengths. No spare vertical sleeve or arm-shaped bulge on the chest; no second forearm attached to the torso, floating cuff, detached hand, impossible bend, stubby arm or third arm. Use image2's running phase for the near-arm swing trajectory. Any far arm remains behind the torso, only naturally visible if occlusion permits; do not invent an extra waist hand. The shoulder patch must travel with the upper arm, not stay pinned as a chest plate. Keep the exact existing whole-body stride, near/far leg order, knees, boots, foot contacts, head/face size and placement, torso lean, narrow build and overall1024canvas registration. Preserve all of image1's matte charcoal quilted suit construction, fine diamond stitching, worn silver straps/hardware and warm brown-haired bearded face, matching images3/4. No brighter grading, glossy rendering, head redesign or body resizing. One coherent whole-figure edit, not pasted body parts. True transparent RGBA, no background/shadow/halo/text/blur. Fixed physical pivot(512,896); do not shift or rescale the figure.'''
 (S/'prompt.txt').write_text(prompt,encoding='utf-8');(S/'references.json').write_text(json.dumps(refs,indent=2)+'\n',encoding='utf-8')
(D/'inherited-sources.json').write_text(json.dumps(inherited,indent=2)+'\n',encoding='utf-8')
print('Two whole-figure arm repairs prepared; four prior sources explicitly inherited.')
