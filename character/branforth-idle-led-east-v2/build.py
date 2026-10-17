from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
import imageio.v2 as iio
from scipy import ndimage
for who in ['branforth']:
 p=Path('character')/(who+'-idle-led-east-v2')
 if not (p/'source.mp4').exists():continue
 def mask(a):
  a=a.astype(float);k=(a[:,:,1]>a[:,:,0]*1.3)&(a[:,:,1]>a[:,:,2]*1.3)&(a[:,:,1]>90);labels,_=ndimage.label(~k);n=np.bincount(labels.ravel());n[0]=0;return labels==n.argmax()
 ref=np.array(Image.open(p/'master-input.png'));ys,xs=np.where(mask(ref));scale=148/(ys.max()-ys.min()+1);offset=(92-round((xs.min()+xs.max())*.5*scale),172-round((ys.max()+1)*scale));reader=iio.get_reader(p/'source.mp4');fps=reader.get_meta_data()['fps'];frames=[]
 for a in reader:
  alpha=mask(a);im=Image.fromarray(np.dstack([a,alpha.astype('uint8')*255]));out=Image.new('RGBA',(184,184));out.alpha_composite(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS),offset);frames.append(out)
 reader.close();dest=p/'frames';dest.mkdir(exist_ok=True)
 sheet=Image.new('RGB',(1104,440),'#303b40');dr=ImageDraw.Draw(sheet)
 for j,n in enumerate(np.linspace(0,len(frames)-1,12).astype(int)):
  sheet.paste(frames[n],(j%6*184,j//6*220+20),frames[n]);dr.text((j%6*184+4,j//6*220+3),str(n),fill='white')
 sheet.save(p/'contact.png');pre=[]
 for n,im in enumerate(frames):
  im.save(dest/f'{n:03}.png');bg=Image.new('RGB',(552,220),'#303b40')
  for h,x in [(148,0),(82,210),(54,350),(27,450)]:
   side=round(184*h/148);small=im.resize((side,side),Image.Resampling.BILINEAR);bg.paste(small,(x,20),small)
  pre.append(bg)
 pre[0].save(p/'review.gif',save_all=True,append_images=pre[1:],duration=round(1000/fps),loop=0)
 (p/'checks.json').write_text(json.dumps({'frames':len(frames),'fps':fps,'fixedScale':scale,'offset':offset,'additionalGrade':False,'loopSelected':False},indent=2))
 (p/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#303b40;color:white;font:18px system-ui;max-width:1000px;margin:auto}img,video{max-width:100%}</style><h1>'+who+' idle-led side walk</h1><p>New source trial from exact idle pose. Full clip, not a selected loop; no additional colour grading. Runtime unchanged.</p><img src="review.gif"><video src="source.mp4" controls loop></video><img src="contact.png">')
 print(who,len(frames))
