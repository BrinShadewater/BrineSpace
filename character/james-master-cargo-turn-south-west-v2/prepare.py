from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];p.mkdir(exist_ok=True)
sources=[r/'character/james-south-master-carry-v1/carry-pose.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
assert not (p/'generation.json').exists()
for name,source in zip(['first','last'],sources):
    im=Image.open(source).convert('RGBA');assert im.size==(256,256)
    bg=Image.new('RGBA',(256,256),'white');bg.alpha_composite(im);bg.convert('RGB').resize((1024,1024),Image.Resampling.NEAREST).save(p/(name+'-input.png'))
prompt='''[Static shot] A finely painted flat 2D game sprite engineer holding a compact horizontal dark grey case with BOTH hands at waist level on a plain white background. Make exactly ONE short QUARTER turn: start facing the viewer/front (South) as first image, finish facing LEFT (West) as last image. Follow the shortest90-degree path, never pass the left-facing terminal pose. Never face right, show the back or perform a full spin. Hold the supplied final left-facing pose after turning.

Keep head size, body height, stocky proportions, muted engineering-yellow patches, grey hair/forehead goggles/horseshoe moustache, matte neutral graphite quilted suit and worn silver fittings consistent with BOTH masters. No purple/magenta, exposure or shiny material change. Belt wrench stays anatomical RIGHT; diagnostic meter anatomical LEFT. Keep both tools on belt, never in hands, no duplication/disappearance. Same compact dark grey case with four silver fittings remains held throughout, no coloured marks; hands never clip through it/body.

Turn torso/head/shoulders/case/legs together naturally, feet rotate locally UNDER the hips without stepping, kicking, spreading out or lifting a foot forward. No walking/stride/kneeling/nod, translation, scale change, camera orbit/zoom, bounce or height drift. Same foot baseline and full canvas margins from first and last inputs, complete body/boots always visible. Case follows the grip smoothly, no torso self-clipping or broken knees. One controlled quarter turn only; static orthographic sprite camera, flat white background, no scene/text/shadow.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=sources+[p/'first-input.png',p/'last-input.png',p/'prompt.txt',r/'tools/minimax_video.py',r/'character/james-south-master-carry-v1/inputs.json',r/'character/james-south-master-carry-v1/review.json',r/'character/james-west-master-carry-v1/local-v3-review.json']
(p/'inputs.json').write_text(json.dumps({'sources':[f.relative_to(r).as_posix() for f in sources],'preCallSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'uniformEnlargement':4,'selected':False,'estimatedUSD':.28,'scope':'Provisional canonical matched bare carrying endpoints; new continuous quarter-turn source candidate,not normal admission.'},indent=2)+'\n',encoding='utf-8')
print('Canonical South/West endpoint inputs uniformly4x white1024, exact prompt/helper/source hashes frozen; one exclusive video submission authorized.')
