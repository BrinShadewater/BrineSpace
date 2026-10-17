from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review';O.mkdir(exist_ok=True);F=O/'video-frames';F.mkdir(exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),25);index=0;clock=0;chapters=[]
with (O/'frames.txt').open('w') as listing:
 for family in ['ground','water']:
  ms={g:json.load(open(P/f'{family}-{g}-manifest.json')) for g in ['bare','helmet']};states={g:{s['id']:s for s in m['states']} for g,m in ms.items()}
  for key,s in states['bare'].items():
   start=clock
   for i,hold in enumerate(s['frameDurationsMs']):
    canvas=Image.new('RGB',(1000,620),'#242c31');d=ImageDraw.Draw(canvas);d.text((18,15),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font,fill='white');d.text((18,52),key+' / paired utility suit / muted cyan',font=font,fill='#bcd6d8')
    for gear,x in [('bare',250),('helmet',750)]:
     im=Image.open(P/states[gear][key]['frameFiles'][i]).convert('RGBA');im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);pivot=ms[gear]['pivot'];anchor=(x-pivot[0]*2,(530 if family=='ground' else 350)-pivot[1]*2);canvas.paste(im,anchor,im)
    name=f'{index:04d}.png';canvas.save(F/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration {hold/1000:.9f}\n");index+=1;clock+=hold/1000
   chapters.append({'state':key,'start':start,'end':clock})
 listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
with (O/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-t',f'{clock:.9f}','-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'death-preview.mp4')],stdout=log,stderr=log,check=True)
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(O/'death-preview.mp4')],text=True));assert abs(encoded-clock)<=1/60
(O/'media.json').write_text(json.dumps({'seconds':clock,'encodedSeconds':encoded,'timebase':'1000fps input clock;60fps output quantization, duration within one video frame','posePairs':index,'source':'Paired48bare/48helmet ground/floating death original source holds; uniformly2x native canvases with original pivots. Sprite replay at60fps (holds quantized to video frames), not continuous station recording.','chapters':chapters},indent=2)+'\n');(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher ground and floating death</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom — ground and floating death</h1><video controls playsinline style="width:100%" src="death-preview.mp4"></video><p>Paired body reuse, original pose holds, uniform native scale. Animation candidates; final station contact review remains.</p><a style="color:cyan" href="death-preview.mp4">Open video directly</a></body>');print(json.dumps({'seconds':clock,'pairs':index,'bytes':(O/'death-preview.mp4').stat().st_size}))
