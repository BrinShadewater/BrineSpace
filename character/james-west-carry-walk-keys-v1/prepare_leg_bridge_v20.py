from pathlib import Path
from PIL import Image
import hashlib, json
p=Path(__file__).resolve().parent; r=p.parents[1]; out=p/'leg-bridge-v20'; out.mkdir(exist_ok=True)
inventory=r/'character/james-full-set-review-2026-10-02/source-inventory.json'
data=json.loads(inventory.read_bytes())
base=r/'character/james-carry-headcaps-v1/frames/004.png'
donor=r/data['states']['bare']['carry-settle-west']['frameFiles'][1]
walk=p/'master-head-review-v16/bare-000.png'
crop=[64,96,208,240]; admission=[88,140,166,228]
refs=[]
for f,label in [(base,'target'),(donor,'pose-guide'),(walk,'walking-reference')]:
    target=out/f'{label}.png'
    Image.open(f).convert('RGBA').crop(crop).resize((576,576),Image.Resampling.LANCZOS).save(target)
    refs.append(target)
prompt='''Use case: precise-object-edit. Edit IMAGE1's lower body only. This is one intermediate standing-to-walking carrying pose for James, not a new character. Image1 is the standing-carry master and owns all art/material/proportions. Image2 is an actual authored motion guide: use ONLY its narrower profile arrangement of hips, knees, shins and planted boots, ignoring its old case, upper suit and belt tools. Image3 is the following walking endpoint and owns recognizable boot/pad/strap detail. Keep image1 upper body, head/collar, shoulder, both arms, both gloves, case and all four latches absolutely unchanged. No new case design or equipment. Below the case, turn the pelvis and legs toward the image2 leg stance: near knee partially occludes far knee rather than two equal front-facing kneepads; far shin and far boot sit behind the near leg, both feet planted naturally. Preserve image2 small near/far separation, upright leg length and stance; do not squat, crouch, bow the knees, cross/fuse legs, kick a foot out or enlarge the boots. Join the hips anatomically to image1 unchanged torso without a black gap or pinched waist. Master matte neutral charcoal grey fabric, muted mustard details, modest dull silver kneepads/straps, soft detailed painted sprite texture. No purple, gloss, bright outlined cartoon, thick black creases, new wrench/meter, or equipment below the glove. Keep same framing and transparent square canvas. These references are the SAME144x144 native crop enlarged4x; fixed full256 canvas/pivot128224/standing ruler148. Ground contact is nativey224 (crop y128), not canvas bottom; do not resize or recenter the character to fill the crop. Retain original master upper body pixels visually; produce one specific profile leg stance below that fixed case. Only lower body changes.'''
pf=out/'prompt.txt';pf.write_text(prompt+'\n',encoding='utf-8')
files=[base,donor,walk,inventory,Path(__file__),p/'package_leg_bridge_v20.py',pf]+refs
inputs=dict(baseFile=base.relative_to(r).as_posix(),donorSource=donor.relative_to(r).as_posix(),donorSlot=1,crop=crop,admissionRegion=admission,
    references=[f.relative_to(r).as_posix() for f in refs],
    preCallSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(out/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n',encoding='utf-8')
print('One lower-body edit prepared; standing upper body/case retained by exact packaging.')
