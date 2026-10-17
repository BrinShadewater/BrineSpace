from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review';O.mkdir(exist_ok=True);F=O/'video-frames';F.mkdir(exist_ok=True);ms={g:{s['id']:s for s in json.load(open(P/(g+'-manifest.json')))['states']} for g in ['bare','helmet']};font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),25);t=0;index=0;chapters=[]
keys=list(ms['bare'])
with (O/'frames.txt').open('w') as listing:
 for key in keys:
  s=ms['bare'][key];start=t;assert s['frameDurationsMs']==ms['helmet'][key]['frameDurationsMs']
  for i,hold in enumerate(s['frameDurationsMs']):
   canvas=Image.new('RGB',(1000,620),'#242c31');draw=ImageDraw.Draw(canvas);draw.text((18,15),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font,fill='white');draw.text((18,52),key+' / utility suit / muted cyan',font=font,fill='#bcd6d8')
   for gear,x in [('bare',0),('helmet',500)]:
    im=Image.open(P/ms[gear][key]['frameFiles'][i]).convert('RGBA').resize((512,512),Image.Resampling.NEAREST);canvas.paste(im,(x,85),im)
   name=f'{index:04d}.png';canvas.save(F/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration {hold/1000:.9f}\n");index+=1;t+=hold/1000
  chapters.append({'state':key,'start':start,'end':t})
 listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
with (O/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-t',f'{t:.9f}','-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'rest-preview.mp4')],stdout=log,stderr=log,check=True)
(O/'media.json').write_text(json.dumps({'seconds':t,'source':'All87bare and87helmet references replayed using original source holds, not continuous station recording','chapters':chapters},indent=2));(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher rest</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom — rest</h1><video controls playsinline style="width:100%" src="rest-preview.mp4"></video><p>Lie down, sleep, get up and bunk transitions. Paired bare and helmet, original body motion and pose holds.</p><a style="color:cyan" href="rest-preview.mp4">Open video directly</a></body>');print(json.dumps({'seconds':t,'poses':index,'bytes':(O/'rest-preview.mp4').stat().st_size}))
