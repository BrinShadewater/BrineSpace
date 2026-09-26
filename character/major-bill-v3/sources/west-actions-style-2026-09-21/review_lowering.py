from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
root=Path.cwd();p=root/'character/major-bill-v3/sources/west-actions-style-2026-09-21';out=root/'output/bill-west-style-2026-09-21/lowering';out.mkdir(parents=True,exist_ok=True)
f=p/'lowering-source.png';a=np.array(Image.open(f).convert('RGBA'));a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;im=Image.fromarray(a);ranges=[(69,243),(343,599),(680,1022),(1041,1400),(1421,1776),(1798,2152)];boxes=[]
for x0,x1 in ranges:
 b=im.crop((x0,0,x1,im.height)).getbbox();boxes.append([x0+b[0],b[1],x0+b[2],b[3]])
scale=148/(boxes[0][3]-boxes[0][1]);records=[];sheet=Image.new('RGB',(1536,280),'#25313a');draw=ImageDraw.Draw(sheet)
for i,b in enumerate(boxes):
 crop=im.crop(b);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST);arr=np.array(crop);yy,xx=np.where(arr[-6:,:,3]>0);toe=int(xx.min());position=(106-toe,224-crop.height);frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop,position);frame.save(out/f'{i:03}.png');sheet.paste(frame,(i*256,18),frame);draw.text((i*256+5,4),str(i),fill='white');records.append({'box':b,'paste':position,'toe_in_crop':toe,'alpha_bounds':frame.getbbox()})
sheet.save(out/'sheet.png');record={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'scale':scale,'alpha_threshold':128,'canvas':[256,256],'pivot':[128,224],'standingHeight':148,'contact_toe':106,'frames':records,'status':'uninstalled lowering candidate; fixed whole-frame toe registration, no limb warping'};(p/'lowering-registration.json').write_text(json.dumps(record,indent=2)+'\n');print(boxes,scale)
