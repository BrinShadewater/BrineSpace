from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review/water';F=O/'video-frames';F.mkdir(exist_ok=True);records=json.load(open(O/'report.json'))['records'];bare=[q for q in records if q['gear']=='bare'];helmet={q['label']:q for q in records if q['gear']=='helmet'};font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24);pairs=[];clock=0.0
with (O/'frames.txt').open('w') as listing:
 for i,q in enumerate(bare):
  h=helmet[q['label']]
  b=Image.new('RGB',(1000,540),'#242c31');d=ImageDraw.Draw(b);d.text((18,12),'KRUSHER DOM / FLOODED STATION / SWIM POSE REVIEW',font=font,fill='white');d.text((18,45),q['label']+' / '+q['action']+' / '+q['direction']+' / time '+str(round(q['time'],2))+'s',font=font,fill='#bcd6d8')
  for col,rec in enumerate([q,h]):
   im=Image.open(O/rec['file']).convert('RGB');px,py=rec['screenFoot'];left=max(0,min(round(px-105),im.width-210));top=max(0,min(round(py-130),im.height-210));crop=im.crop((left,top,left+210,top+210)).resize((420,420),Image.Resampling.NEAREST);b.paste(crop,(40+col*500,95))
  name=f'{i:03d}.png';b.save(F/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration 0.300000000\n");pairs.append({'label':q['label'],'action':q['action'],'bare':q['file'],'helmet':h['file']});clock+=.3
 listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
with (O/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-t',str(clock),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'station-water-review.mp4')],stdout=log,stderr=log,check=True)
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(O/'station-water-review.mp4')],text=True));assert abs(encoded-clock)<=1/60
(O/'media.json').write_text(json.dumps({'seconds':clock,'encodedSeconds':encoded,'pairs':pairs,'scope':'Paired native furnished-room swim and low-air snapshots, each displayed300ms, uniform2x cropped detail. A pose gallery with simulation timestamps, not continuous motion recording or source pose-hold replay.'},indent=2)+'\n')
(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher water review</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom - flooded station pose review</h1><video controls playsinline style="width:100%" src="station-water-review.mp4"></video><p>Native pose gallery: furnished-room movement, low-air distress and restored-air poses. Each snapshot displays300ms.</p></body>')
print(json.dumps({'seconds':clock,'encodedSeconds':encoded,'pairs':len(pairs)}))

board=Image.new('RGB',(1000,2160),'#242c31');d=ImageDraw.Draw(board)
for row,direction in enumerate(['east','west','south','north']):
 pair=next(i for i,q in enumerate(bare) if q['label']==direction+'-distress-060')
 board.paste(Image.open(F/f'{pair:03d}.png'),(0,row*540))
board.save(O/'water-distress-contact-sheet.png')
