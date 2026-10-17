from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'start-bridge-v15';out.mkdir(exist_ok=True)
standing=r/'character/james-carry-headcaps-v1/frames/004.png'
walking=p/'walk00-case-master-v5.png'
original=r/'character/james-west-master-carry-v1/local-original.png'
crop=[64,96,208,240];rect=[88,104,166,228]
for slot in (1,2):
 name=f'start-{slot:03}';refs=[];files=[standing,walking,original,Path(__file__),p/'package_start_bridge_v15.py']
 for f,label in [(standing,'target'),(walking,'walk-reference'),(original,'body-master')]:
  target=out/f'{name}-{label}.png';Image.open(f).convert('RGBA').crop(crop).resize((576,576),Image.Resampling.LANCZOS).save(target);refs.append(target);files.append(target)
 progression='one-third' if slot==1 else 'two-thirds'
 prompt=f'''Edit image1 only: one James West carrying start transition, {progression} of the short weight shift from image1 standing-carry stance into image2 actual walk phase0. Both images have identical144x144 native crop framing enlarged4x, fixed full256 canvas pivot128224, standing body ruler148. Image3 is the original selected standing body master for clothing detail, proportions and neutral matte material, not a request to lower his hands. Produce ONE coherent in-between, not a sheet. Narrow the existing stance gradually toward image2: thighs/knee pads/shins/boots retain anatomy and original sizes, hips and torso turn only the small amount needed between the two poses. Boots remain planted or make a tiny close-in weight adjustment; no kicked-out foot, leg crossing, deep bend, stepping away, kneeling or height bob. Ground/boot sole stays at original native y224 (crop y128), no downward overshoot or whole-body scaling. Keep the same rigid graphite case at low waist in front toward LEFT, same modest depth, small dull silver four corner latches and coherent two-hand grip. Case/arms only settle gently between images1/2, not a new carry action or case bounce. Head/collar, shoulder detail, neutral matte grey/yellow cloth, straps, kneepad size and boot design retain the original master. Preserve anatomical-left high belt meter and natural carrying-hand occlusion, far anatomical-right wrench body-occluded; no new near-side wrench, silver loop or duplicate meter. Do not copy the original master lowered arm. No black holes, purple cast, glossy finish, thick graphic outlines, new costume, per-pose size fitting or camera change. Return full square image1 crop at the identical framing, with body/stance intermediate and transparent background. Keep all cropped image boundaries/head/neck outside the edited body unchanged.'''
 pf=out/f'{name}-prompt.txt';pf.write_text(prompt+'\n',encoding='utf-8');files.append(pf)
 (out/f'{name}-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},'crop':crop,'admissionRegion':rect,'baseFile':standing.relative_to(r).as_posix(),'references':[f.relative_to(r).as_posix() for f in refs],'scope':'One authored planted weight-shift bridge interior; no per-pose fitting. Standing reference provisional. Source/raw body density, case grip, boots and motion acceptance require review.'},indent=2)+'\n')
print('Two planted carry-start interiors prepared; exact existing endpoints preserved.')
