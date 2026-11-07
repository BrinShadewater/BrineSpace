from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path('character/major-bill-v3/sources/west-work-identity-2026-09-21')
a=np.array(Image.open(p/'generated-source.png').convert('RGBA'));a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;im=Image.fromarray(a)
cells=[im.crop((0,0,768,1024)),im.crop((768,0,1536,1024))];boxes=[x.getbbox() for x in cells]
idle=Image.open(p/'canonical-idle.png').convert('RGBA');bounds=idle.getbbox();height=bounds[3]-bounds[1];scale=height/(boxes[0][3]-boxes[0][1]);rows=[]
for name,cell,box in zip(['standing','kneeling'],cells,boxes):
 crop=cell.crop(box);size=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(size,Image.Resampling.LANCZOS);a=np.array(crop);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;crop=Image.fromarray(a)
 out=Image.new('RGBA',(256,256));pos=(106,223-size[1]);out.alpha_composite(crop,pos);out.save(p/(name+'.png'));rows.append({'name':name,'box':box,'size':size,'paste':pos})
(p/'registration.json').write_text(json.dumps({'source_sha256':hashlib.sha256((p/'generated-source.png').read_bytes()).hexdigest(),'scale':scale,'canonical_bounds':bounds,'alpha_threshold':128,'frames':rows},indent=2))
b=Image.new('RGB',(880,260),(23,33,41));d=ImageDraw.Draw(b)
refs=[('Canonical idle',p/'canonical-idle.png'),('Study standing',p/'standing.png'),('Current kneeling',Path('character/major-bill-v3/frames/bare/kneel-west/005.png')),('Study kneeling',p/'kneeling.png')]
for i,(label,f) in enumerate(refs):
 x=Image.open(f).convert('RGBA')
 if i==0:
  can=Image.new('RGBA',(256,256));can.alpha_composite(x,(36,52));x=can
 x=x.crop((40,54,240,236));b.paste(x,(i*220,0),x);d.text((i*220+5,210),label,fill='white')
b.save(p/'identity-review.png');print('Calibration',height,rows)
