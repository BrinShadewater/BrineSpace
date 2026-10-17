from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
source=r/'character/james-carry-headcaps-v1/frames/004.png'
base=Image.open(source).convert('RGBA');base.save(p/'base.png')
crop=(88,152,176,240)
base.crop(crop).resize((704,704),Image.Resampling.LANCZOS).save(p/'legs-target.png')
base.resize((1024,1024),Image.Resampling.LANCZOS).save(p/'whole-reference.png')
prompt='''Edit IMAGE 1, a fixed88x88 native square lower-body crop enlarged8x. IMAGE 2 is only the whole James carrying pose for camera, trousers and style. Return the same square crop with its original margins, transparent background. Do not zoom, shift framing, add a torso or recenter.
Create ONE modest walking CONTACT pose facing image LEFT, carrying a heavy case: near leg reaches forward to image LEFT, far leg reaches backward to image RIGHT. Keep hip attachment and upper trouser positions unchanged at the top; knees bend anatomically, two intact separate legs, unchanged knee pad/boot design. Near forward heel touches the existing sole baseline at native y224 (crop y72); far rear toe touches that same baseline with heel slightly lifted. Near sole center approx native x112 (crop x24), far toe approx x151 (crop x63), avoiding huge stride. Preserve two distinct boots, believable weight and full ankle attachment. No third leg, no rubber knees, no disconnected shin, no deep squat. Walking leg movement, not twisting the torso. Do not duplicate a belt device. Keep all pelvis/tool pixels above native y172 (crop y20) unchanged.
Use precisely the subdued matte graphite cloth, muted ochre details and worn silver boots of IMAGE 1. No purple/magenta, exposure lift, glossy metal, added black cavity, pale edge or shadow puddle. Fine painted game sprite, not smooth vector or photorealism. Genuine alpha transparency. Every unchanged pixel stays at the target position. This is an independently drawn gait source, not a resized whole pose.'''
(p/'contact-a-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=[source,p/'base.png',p/'legs-target.png',p/'whole-reference.png',p/'contact-a-prompt.txt',Path(__file__)]
(p/'contact-a-inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'crop':crop,'admissionRegion':[88,172,176,224],'scope':'First contact draft only; remaining cycle/body dynamics/native contexts pending.'},indent=2)+'\n',encoding='utf-8')
print('Master-based West lower-body target and source/prompt inventory prepared.')
