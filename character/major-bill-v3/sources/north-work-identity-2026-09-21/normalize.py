from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path('character/major-bill-v3/sources/north-work-identity-2026-09-21')
a=np.array(Image.open(p/'generated-source.png').convert('RGBA'));a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255
im=Image.fromarray(a);left=im.crop((0,0,768,1024));right=im.crop((768,0,1536,1024))
boxes=[x.getbbox() for x in (left,right)];scale=151/(boxes[0][3]-boxes[0][1]);rows=[]
for name,cell,box in zip(['standing','kneeling'],[left,right],boxes):
 crop=cell.crop(box);size=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(size,Image.Resampling.LANCZOS)
 pix=np.array(crop);pix[pix[:,:,3]<128]=0;pix[pix[:,:,3]>=128,3]=255;crop=Image.fromarray(pix)
 out=Image.new('RGBA',(256,256));pos=(128-size[0]//2,224-size[1]);out.alpha_composite(crop,pos);out.save(p/(name+'.png'));rows.append({'name':name,'box':box,'size':size,'paste':pos})
(p/'registration.json').write_text(json.dumps({'source_sha256':hashlib.sha256((p/'generated-source.png').read_bytes()).hexdigest(),'scale':scale,'alpha_threshold':128,'filter':'LANCZOS; binary alpha128 before and after','frames':rows},indent=2))
b=Image.new('RGB',(768,270),(23,33,41));d=ImageDraw.Draw(b)
for i,(label,f) in enumerate([('Canonical idle',p/'canonical-idle.png'),('Study standing',p/'standing.png'),('Study kneeling',p/'kneeling.png')]):
 x=Image.open(f).convert('RGBA')
 if i==0:
  can=Image.new('RGBA',(256,256));can.alpha_composite(x,(36,52));x=can
 b.paste(x,(i*256,0),x);d.text((i*256+12,240),label,fill='white')
b.save(p/'identity-review.png');print(rows)
