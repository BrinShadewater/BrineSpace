from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review/galley';F=O/'video-frames';F.mkdir(exist_ok=True)
r=json.load(open(O/'report.json'));progress=json.load(open(R/'character/krusher-complete-animation-v1/progress.json'));font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),23);clock=0.;entries=[];manifest_cache={}
with (O/'frames.txt').open('w') as listing:
 for i,q in enumerate(r['records']):
  b=Image.new('RGB',(1000,540),'#242c31');d=ImageDraw.Draw(b);d.text((18,12),'KRUSHER DOM / GALLEY SERVICE / '+q['gear'].upper(),font=font,fill='white');d.text((18,43),q['label']+' / '+q['direction']+' / time '+str(round(q['time'],2))+'s',font=font,fill='#bcd6d8')
  im=Image.open(O/q['file']).convert('RGB');px,py=q['screenFoot'];left=max(0,min(round(px-105),im.width-210));top=max(0,min(round(py-130),im.height-210));crop=im.crop((left,top,left+210,top+210)).resize((420,420),Image.Resampling.NEAREST);b.paste(crop,(30,95));d.text((525,90),'Selected source / native1x',font=font,fill='#bcd6d8')
  key=q['source']['key'];idx=q['source']['index'];mp=R/progress['coverage'][q['gear']]['available'][key]['manifest'][6:]
  if str(mp) not in manifest_cache:manifest_cache[str(mp)]=json.load(open(mp))
  m=manifest_cache[str(mp)];state=next(x for x in m['states'] if x['id']==key);path=state['frameFiles'][idx];path=R/path[6:] if path.startswith('res://') else mp.parent/path;src=Image.open(path).convert('RGBA');bg=Image.new('RGBA',src.size,'#242c31');bg.alpha_composite(src);b.paste(bg.convert('RGB'),(round(750-m['pivot'][0]),round(360-m['pivot'][1])));d.text((525,485),key+' / pose '+str(idx),font=font,fill='#bcd6d8')
  name=f'{i:03d}.png';b.save(F/name);listing.write(f"file 'video-frames/{name}'\noption framerate 1000\nduration 0.200000000\n");clock+=.2;entries.append({'record':q['file'],'time':q['time'],'source':str(path),'key':key,'index':idx})
 listing.write(f"file 'video-frames/{name}'\noption framerate 1000\n")
with (O/'media.log').open('w') as log:subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(O/'frames.txt'),'-t',str(clock),'-vf','fps=60','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'station-galley-review.mp4')],stdout=log,stderr=log,check=True)
encoded=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(O/'station-galley-review.mp4')],text=True));assert abs(encoded-clock)<=1/60
(O/'media.json').write_text(json.dumps({'seconds':clock,'encodedSeconds':encoded,'samples':entries,'scope':'All132native galley snapshots, actual scene cropped uniformly2x alongside selected source at native1x and registered pivot;200ms/sample, gallery not continuous movement/source-hold replay.'},indent=2)+'\n')
(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>Krusher galley review</title><body style="background:#242c31;color:#cadcde;font:18px sans-serif;max-width:1000px;margin:24px auto"><h1>Krusher Dom - galley service</h1><video controls playsinline style="width:100%" src="station-galley-review.mp4"></video><p>Native pose gallery: food/cup handoffs, meal and sip; sealed helmet uses inspection.</p></body>')
board=Image.new('RGB',(1000,2160),'#242c31')
for quarter in range(4):
 i=next(i for i,q in enumerate(r['records']) if q['quarter']==quarter and q['gear']=='bare' and q['action']=='eat' and q['time']>=2)
 board.paste(Image.open(F/f'{i:03d}.png'),(0,quarter*540))
board.save(O/'galley-contact-sheet.png');print(json.dumps({'seconds':clock,'encodedSeconds':encoded,'samples':len(entries)}))
