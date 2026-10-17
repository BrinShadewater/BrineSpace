from pathlib import Path
import argparse,json,shutil
from PIL import Image,ImageDraw
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--start',type=int,required=True);ap.add_argument('--end',type=int,required=True);ap.add_argument('--direction',choices=['east','west'],default='east');a=ap.parse_args();src=Path(a.source);p=Path(a.output);p.mkdir(exist_ok=True);ids=list(range(a.start,a.end));fps=json.loads((src/'checks.json').read_text())['fps'];preview=[];sheet=Image.new('RGB',(1104,440),'#303b40');draw=ImageDraw.Draw(sheet)
for j,n in enumerate(ids):
 im=Image.open(src/'frames'/f'{n:03}.png').convert('RGBA');dest=p/'frames'/f'{j:03}.png';dest.parent.mkdir(exist_ok=True);shutil.copyfile(src/'frames'/f'{n:03}.png',dest);bg=Image.new('RGB',(552,220),'#303b40')
 for height,x in [(148,0),(82,210),(54,350),(27,450)]:
  side=round(184*height/148);sm=im.resize((side,side),Image.Resampling.BILINEAR);bg.paste(sm,(x,20),sm)
 preview.append(bg)
for j,n in enumerate(np.linspace(ids[0],ids[-1],12).astype(int)):
 im=Image.open(src/'frames'/f'{n:03}.png');sheet.paste(im,(j%6*184,j//6*220+20),im);draw.text((j%6*184+4,j//6*220+3),str(n),fill='white')
dur=[round((i+1)*1000/fps)-round(i*1000/fps) for i in range(len(ids))];preview[0].save(p/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*100/fps)-round(i*100/fps)) for i in range(len(ids))],loop=0);sheet.save(p/'contact.png');m=dict(name=p.name,frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,precomposed=True,textureFilter='linear',states=[dict(id='walk-'+a.direction,loop=True,gaitCycles=1,frameCount=len(ids),frameFiles=[f'frames/{i:03}.png' for i in range(len(ids))],frameDurationsMs=dur,sourceFrames=ids,provenance={'source':str(src),'method':'Exact copies, original speed, no interpolation or resizing.'})]);(p/'manifest.json').write_text(json.dumps(m,indent=2));(p/'index.html').write_text('<!doctype html><style>body{background:#303b40;color:white;font:18px system-ui}img{max-width:100%}</style><h1>'+p.name+'</h1><p>Loop candidate; original timing, no frames synthesized. Runtime unchanged.</p><img src="review.gif"><img src="contact.png">');print(len(ids),sum(dur))
