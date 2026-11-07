from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path('character/major-bill-v3/sources/west-actions-style-2026-09-21');im=Image.open(p/'pair-source.png').convert('RGBA');a=np.array(im);print(im.size,np.unique(a[:,:,3],return_counts=True)[0][::32]);out=Path('output/bill-west-style-2026-09-21');out.mkdir(exist_ok=True)
a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;im=Image.fromarray(a);boxes=[]
for x0,x1 in ((0,700),(700,1536)):
 box=im.crop((x0,0,x1,1024)).getbbox();boxes.append([box[0]+x0,box[1],box[2]+x0,box[3]])
scale=148/(boxes[0][3]-boxes[0][1]);canvas=Image.new('RGB',(768,280),'#25313a');d=ImageDraw.Draw(canvas)
for i,(name,img) in enumerate([('canonical standing',Image.open('character/major-bill-v3/frames/bare/idle-west/000.png').convert('RGBA')),('study standing',None),('current work',Image.open('character/major-bill-v3/frames/bare/repair-west/000.png').convert('RGBA')),('study work',None)]):
 if img is None:
  j=0 if i==1 else 1;crop=im.crop(boxes[j]);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST);img=Image.new('RGBA',(256,256));img.alpha_composite(crop,(128-crop.width//2,224-crop.height));img.save(out/('standing.png' if j==0 else 'work.png'));pivot=(128,224)
 else:pivot=(92,172) if i==0 else (128,224)
 canvas.paste(img,(i*192+96-pivot[0],245-pivot[1]),img);d.text((i*192+5,8),name,fill='white')
canvas.save(out/'same-scale.png');record={'provider':'built-in image_gen','sha256':hashlib.sha256((p/'pair-source.png').read_bytes()).hexdigest(),'boxes':boxes,'scale':scale,'alpha_threshold':128,'status':'uninstalled representative standing/work study; needs contact and identity review'};(p/'pair-registration.json').write_text(json.dumps(record,indent=2)+'\n');print(boxes,scale)
