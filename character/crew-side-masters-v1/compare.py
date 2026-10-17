from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent
specs=[('Bill',P/'bill-side-master-01.png'),('Veld',P.parent/'veld-side-foundation-v1/side-master-01.png'),('Branforth',P/'branforth-side-master-02.png')]
out=Image.new('RGB',(1080,1180),'#263139');d=ImageDraw.Draw(out);records=[]
for col,(name,path) in enumerate(specs):
 im=Image.open(path).convert('RGBA');a=np.array(im);d.text((col*360+20,12),name+(' / APPROVED' if name=='Veld' else ' / CANDIDATE'),fill='white')
 for row in range(2):
  left=row*(im.width//2);part=a[:,left:left+im.width//2];ys,xs=np.where(part[:,:,3]>=128);box=(left+int(xs.min()),int(ys.min()),left+int(xs.max())+1,int(ys.max())+1)
  crop=im.crop(box);b=np.array(crop);b[:,:,3]=np.where(b[:,:,3]>=128,255,0);crop=Image.fromarray(b);crop=crop.resize((round(crop.width*470/crop.height),470),Image.Resampling.LANCZOS);x=col*360+(360-crop.width)//2;y=row*580+55;out.paste(crop,(x,y),crop)
  small=crop.resize((round(crop.width*74/470),74),Image.Resampling.LANCZOS);out.paste(small,(col*360+170-small.width//2,y+478),small)
  records.append(dict(actor=name,direction='east' if row==0 else 'west',source=str(path),crop=box,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),sourceAlphaRange=[int(a[:,:,3].min()),int(a[:,:,3].max())]))
out.save(P/'cast-comparison.png');(P/'review.json').write_text(json.dumps({'status':'visual-review candidates, not installed or design locked','comparison':'470px standing height and74px thumbnail, alpha128 removes faint source haze in review only. Original masters unchanged.','sources':records},indent=2)+'\n')
