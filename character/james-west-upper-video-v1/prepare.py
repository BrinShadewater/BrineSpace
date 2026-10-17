from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1]
sources=[r/'character/james-east-cargo-heads-v3/frames/bare/carry-turn-east-west/010.png',r/'character/james-cargo-material-joined-v1/frames/bare/unload-west/000.png']
for name,source in zip(['first','last'],sources):
    im=Image.open(source).convert('RGBA');assert im.size==(256,256)
    crop=im.crop((96,56,176,136));bg=Image.new('RGBA',(80,80),'white');bg.alpha_composite(crop)
    bg.convert('RGB').resize((640,640),Image.Resampling.NEAREST).save(p/(name+'-input.png'))
prompt='''[Static shot] A flat finely painted 2D game sprite upper-body crop, white background. Interpolate smoothly from supplied first pose to supplied last pose using the SHORTEST tiny pose adjustment. This is a left-facing engineer changing from profile-left to slightly three-quarter-left, only a few degrees. Head, neck, collar and near shoulder adjust together naturally; only minimal local articulation. Keep the face looking left throughout. NEVER show the back of his head or backpack rear; never turn right or face the camera. No rotation around the character, full spin, sweeping turn, nod, translation, camera movement or zoom. Keep original square crop margins and head size/height fixed. Same mature face, grey-brown hair, forehead goggles, moustache, muted yellow shoulder patch and matte graphite suit/backpack, same symbols. Preserve native finely painted detail density and subdued neutral colour. No shiny finish, purple/pink grade, brighter exposure, changing anatomy or new insignia. Shoulder patch must stay attached to the same sleeve and backpack equipment stay on the same side. Make one very slight continuous adjustment into supplied last pose and hold. No extra motion, text, borders or scene. Do not reveal lower body or extend the crop.'''
(p/'prompt.txt').write_text(prompt+'\n',encoding='utf-8')
files=sources+[p/'first-input.png',p/'last-input.png',p/'prompt.txt',r/'tools/minimax_video.py']
(p/'inputs.json').write_text(json.dumps({'sources':[x.relative_to(r).as_posix() for x in sources],'crop':[96,56,176,136],'uniformEnlargement':8,'preCallSha256':{x.relative_to(r).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in files},'selected':False,'estimatedUSD':.28},indent=2)+'\n')
print('Exact native80-square upper endpoints uniformly8x on white;source/prompt/helper hashes frozen.')
