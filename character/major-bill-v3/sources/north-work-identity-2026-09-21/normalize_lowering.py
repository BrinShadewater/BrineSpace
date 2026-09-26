from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path('character/major-bill-v3/sources/north-work-identity-2026-09-21')
a=np.array(Image.open(p/'lowering-source.png').convert('RGBA'));a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;im=Image.fromarray(a)
boxes=[];cells=[]
for i in range(6):
 rect=((i%3)*512,0 if i<3 else 550,(i%3+1)*512,550 if i<3 else 1024)
 cell=im.crop(rect);box=cell.getbbox();cells.append(cell);boxes.append(box)
scale=151/(boxes[0][3]-boxes[0][1]);rows=[]
for i,(cell,box) in enumerate(zip(cells,boxes)):
 crop=cell.crop(box);size=(round(crop.width*scale),round(crop.height*scale));crop=crop.resize(size,Image.Resampling.LANCZOS);a=np.array(crop);a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;crop=Image.fromarray(a)
 out=Image.new('RGBA',(256,256));paste=(128-size[0]//2,224-size[1]);out.alpha_composite(crop,paste);out.save(p/f'lowering-{i:03}.png');rows.append({'cell':[(i%3)*512,0 if i<3 else 550,(i%3+1)*512,550 if i<3 else 1024],'box':box,'size':size,'paste':paste})
 if i==5:cell.crop(box).save(p/'work-reference.png')
(p/'lowering-registration.json').write_text(json.dumps({'source_sha256':hashlib.sha256((p/'lowering-source.png').read_bytes()).hexdigest(),'scale':scale,'alpha_threshold':128,'filter':'LANCZOS; binary alpha128 before and after','frames':rows},indent=2))
b=Image.new('RGB',(1056,210),(23,33,41));d=ImageDraw.Draw(b)
for i in range(6):
 f=Image.open(p/f'lowering-{i:03}.png').crop((40,54,216,236));b.paste(f,(i*176,0),f);d.text((i*176+8,188),str(i),fill='white')
b.save(p/'lowering-review.png');print(rows)
