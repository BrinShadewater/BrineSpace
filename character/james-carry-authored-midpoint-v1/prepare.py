from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[r/'character/james-south-master-carry-v1/carry-pose.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
for name,source in zip(['south-reference','west-reference'],sources):
    im=Image.open(source).convert('RGBA');assert im.size==(256,256)
    im.resize((1024,1024),Image.Resampling.NEAREST).save(p/(name+'.png'))
prompt='''Create ONE transparent whole-body sprite pose of this exact engineer, James, halfway between the supplied front/South and left/West carrying poses. Both images are reference images, NOT separate characters or a sheet to reproduce. One single figure on the exact same square canvas and at the same scale as these references. View faces diagonally toward the lower-left/viewer-left, exactly45degrees from front toward left; his face, chest, hips, knees and boots all turn together. We see his front and left-facing profile in equal measure. Never turn toward the right or show his back.

Preserve stocky adult anatomy, compact head, grey hair, forehead yellow goggles, moustache, fine hand-painted 2D orthographic game-sprite treatment. Neutral matte graphite quilted suit, muted mustard-yellow engineering patches, worn silver fittings. Same subdued exposure/material as references; no shiny highlights, purple/magenta, pure black shadow masses or invented backpack colours. Same head height, shoulder-to-hip and leg proportions; no shortening/stretching.

Hold the SAME compact horizontal graphite case in BOTH hands directly in front of waist; case rotates diagonally with torso. Fingers visibly grasp opposite ends; four restrained silver case fittings, no redesign or extra tools. Belt wrench anatomical RIGHT, diagnostic meter anatomical LEFT, naturally partly occluded by forearms/case. No tool in hands or duplicate meter. Backpack stays close to spine.

Pose is stationary during a local quarter turn: both boots flat on same floor baseline, knees intact, legs under hips, no stride, crossed legs, lifted foot, extended toe, crouch or forward lean. Keep the exact original reference composition: crown at29.7percent canvas height, soles at87.5percent, overall standing148/256 height, physical ground pivot at50percent/87.5percent. Full body at same size; generous original transparent margins. Do not crop or zoom/fit to figure. No scene, lettering, guide marks, extra frames or shadows. Genuine transparent alpha. This is a controlled intermediate whole-body orientation, not a copy of either endpoint.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=sources+[p/'south-reference.png',p/'west-reference.png',p/'prompt.txt',Path(__file__)]
(p/'inputs.json').write_text(json.dumps({'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'targetAngleDegrees':45,'uniformReferenceEnlargement':4,'sourceCanvas':[256,256],'standingRuler':148,'pivot':[128,224],'selected':False,'scope':'Single bare whole-body carried midpoint source; geometry and material require review, no normal admission.'},indent=2)+'\n',encoding='utf-8')
print('Two exact uniformly enlarged pose references and single midpoint prompt frozen.')
