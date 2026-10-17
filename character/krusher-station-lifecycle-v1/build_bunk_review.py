from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review/bunk';F=O/'video-frames';F.mkdir(exist_ok=True);r=json.load(open(O/'report.json'));records=r['records'];bare=[q for q in records if q['gear']=='bare'];helmet={(q['key'],q['pose']):q for q in records if q['gear']=='helmet'};clock=0.0;chapters=[];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
with (O/'frames.txt').open('w') as listing:
 for i,q in enumerate(bare):
  b=Image.new('RGB',(1000,560),'#242c31');d=ImageDraw.Draw(b);d.text((18,10),'KRUSHER DOM / SYSTEM ADMINISTRATOR / STATION BUNK',font=font,fill='white');d.text((18,42),q['key']+' / pose'+str(q['pose'])+' / bare and helmet',font=font,fill='#bcd6d8')
  for col,rec in enumerate([q,helmet[(q['key'],q['pose'])]]):
   im=Image.open(O/rec['file']).convert('RGB');assert im.width>=450 and im.height>=450,'Full room camera required';im.thumbnail((480,480));b.paste(im,(10+col*500,78))
  name=f'{i:03d}.png';b.save(F/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration {q['hold']:.9f}\n");chapters.append({'key':q['key'],'pose':q['pose'],'start':clock,'duration':q['hold']});clock+=q['hold']
 listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
with (O/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-t',str(clock),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'station-bunk-preview.mp4')],stdout=log,stderr=log,check=True)
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(O/'station-bunk-preview.mp4')],text=True));assert abs(encoded-clock)<=1/60
(O/'media.json').write_text(json.dumps({'seconds':clock,'encodedSeconds':encoded,'pairs':len(bare),'chapters':chapters,'scope':'All paired native station bunk poses at registered controller times; source hold replay60fps, no continuous station recording.'},indent=2)+'\n')
(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher station bunk</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom - station bunk test</h1><video controls playsinline style="width:100%" src="station-bunk-preview.mp4"></video><p>Native station poses, original pose holds. Paired bare and helmet. Prescribed replay.</p></body>')
print(json.dumps({'seconds':clock,'encodedSeconds':encoded,'pairs':len(bare)}))
