from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review/chairs';F=O/'video-frames';F.mkdir(exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24);clock=0.0;chapters=[];index=0
with (O/'frames.txt').open('w') as listing:
 for room in ['crew_lounge','observation_room']:
  records=json.load(open(O/room/'report.json'))['records'];bare=[q for q in records if q['gear']=='bare'];helm={(q['quarter'],q['key'],q['pose']):q for q in records if q['gear']=='helmet'}
  for rec in bare:
   b=Image.new('RGB',(1000,540),'#242c31');d=ImageDraw.Draw(b);d.text((18,12),'KRUSHER DOM / STATION CHAIRS AND TABLET',font=font,fill='white');d.text((18,45),room+' / q'+str(rec['quarter'])+' / '+rec['key']+' / pose'+str(rec['pose']),font=font,fill='#bcd6d8')
   for col,q in enumerate([rec,helm[(rec['quarter'],rec['key'],rec['pose'])]]):
    im=Image.open(O/room/q['file']).convert('RGB');assert im.width>=420 and im.height>=420
    local=[q['foot'][i]-7872+q['offset'][i] for i in range(2)];px=(local[0]+192)*im.width/384;py=(local[1]+192)*im.height/384
    left=max(0,min(round(px-105),im.width-210));top=max(0,min(round(py-125),im.height-210));crop=im.crop((left,top,left+210,top+210)).resize((420,420),Image.Resampling.NEAREST);b.paste(crop,(40+col*500,95));d.text((45+col*500,76),'bare' if col==0 else 'helmet',fill='white')
   name=f'{index:04d}.png';b.save(F/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration {rec['hold']:.9f}\n");chapters.append({'room':room,'quarter':rec['quarter'],'key':rec['key'],'pose':rec['pose'],'start':clock,'duration':rec['hold']});clock+=rec['hold'];index+=1
 listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
with (O/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-t',str(clock),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'station-chairs-tablet-preview.mp4')],stdout=log,stderr=log,check=True)
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(O/'station-chairs-tablet-preview.mp4')],text=True));assert abs(encoded-clock)<=1/60
(O/'media.json').write_text(json.dumps({'seconds':clock,'encodedSeconds':encoded,'pairs':index,'chapters':chapters,'scope':'Every paired native chair/tablet pose from two rooms/four rotations, source holds replay60fps; cropped station detail at uniform2x, no continuous station recording claim.'},indent=2)+'\n')
(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher station chairs and tablet</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom - station chairs and tablet</h1><video controls playsinline style="width:100%" src="station-chairs-tablet-preview.mp4"></video><p>Paired native station pose replay, original holds, detail enlarged2x.</p></body>')
print(json.dumps({'seconds':clock,'encodedSeconds':encoded,'pairs':index}))
