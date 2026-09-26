from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
root=Path.cwd();source=root/'character/major-bill-v3/sources/west-actions-style-2026-09-21';out=root/'output/bill-west-style-2026-09-21';(out/'work').mkdir(exist_ok=True)
a=np.array(Image.open(source/'work-source.png').convert('RGBA'));a[a[:,:,3]<128]=0;a[a[:,:,3]>=128,3]=255;im=Image.fromarray(a);base=Image.open(out/'lowering/005.png').convert('RGBA');poly=[(100,138),(136,138),(138,149),(150,155),(169,158),(169,171),(158,175),(133,170),(109,161),(100,151)];mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon(poly,fill=255);scale=111/489;frames=[]
for i in range(6):
 pose=base.copy()
 if i not in (0,5):
  crop=im.crop((i*362,0,(i+1)*362,724));crop=crop.resize((round(362*scale),round(724*scale)),Image.Resampling.NEAREST);registered=Image.new('RGBA',(256,256));registered.alpha_composite(crop,(103,81));pose.paste(registered,(0,0),mask)
 pose.save(out/'work'/f'{i:03}.png');frames.append(pose)
 assert np.array_equal(np.array(pose)[np.array(mask)==0],np.array(base)[np.array(mask)==0])
sheet=Image.new('RGB',(1536,256),'#25313a')
for i,f in enumerate(frames):sheet.paste(f,(i*256,0),f)
sheet.save(out/'work/sheet.png');(source/'work-registration.json').write_text(json.dumps({'sha256':hashlib.sha256((source/'work-source.png').read_bytes()).hexdigest(),'cell_width':362,'scale':scale,'paste':[103,81],'replacement_polygon':poly,'endpoints':'settled lowering pose unchanged','status':'uninstalled arm-only composite study'},indent=2)+'\n')
print('6 work frames; head, torso outside arm mask and all legs remain pixel-identical; endpoints exact')
