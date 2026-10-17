from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review';O.mkdir(exist_ok=True);F=O/'video-frames';F.mkdir(exist_ok=True)
ms={g:json.loads((P/(g+'-manifest.json')).read_text()) for g in ['bare','helmet']};states={g:{s['id']:s for s in m['states']} for g,m in ms.items()};font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24);t=0;index=0;chapters=[]
with (O/'frames.txt').open('w') as listing:
 for d in ['south','east','north','west']:
  for action in ['sit-down','sit-idle','read-seated-enter','read-seated','read-seated-exit','sit-rise']:
   key=action+'-'+d;s=states['bare'][key];hs=states['helmet'][key];start=t
   assert s['frameDurationsMs']==hs['frameDurationsMs']
   for i,hold in enumerate(s['frameDurationsMs']):
    canvas=Image.new('RGB',(800,500),'#242c31');draw=ImageDraw.Draw(canvas);draw.text((18,16),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font,fill='white');draw.text((18,53),key+' / James utility suit / muted cyan',font=font,fill='#bbd7d9')
    for g,x in [('bare',45),('helmet',425)]:
     im=Image.open(P/states[g][key]['frameFiles'][i]).convert('RGBA').resize((368,384),Image.Resampling.NEAREST);canvas.paste(im,(x,100),im)
    name=f'{index:04d}.png';canvas.save(F/name);listing.write(f"file 'video-frames/{name}'\nduration {hold/1000:.9f}\n");index+=1;t+=hold/1000
   chapters.append({'state':key,'start':round(start,6),'end':round(t,6)})
 listing.write(f"file 'video-frames/{name}'\n")
with (O/'media.log').open('w') as log:
 subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'seated-preview.mp4')],stdout=log,stderr=log,check=True)
(O/'media.json').write_text(json.dumps({'source':'All144bare poses paired with matching144helmet poses; manifest holds; rendered sprite replay, not continuous station recording','seconds':t,'chapters':chapters},indent=2))
(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher seated</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom — repair</h1><video controls playsinline style="width:100%" src="seated-preview.mp4"></video><p>Sit, read, rise: four directions, bare and helmet. Original body motion and pose timing.</p><a style="color:cyan" href="seated-preview.mp4">Open video directly</a></body>')
print(json.dumps({'seconds':t,'poses':index,'bytes':(O/'seated-preview.mp4').stat().st_size}))
