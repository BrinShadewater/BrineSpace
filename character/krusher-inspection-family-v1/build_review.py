from pathlib import Path
import json,math,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review';O.mkdir(exist_ok=True);bare=json.loads((P/'bare-manifest.json').read_text());helmet=json.loads((P/'helmet-manifest.json').read_text());font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24);video=O/'inspection-preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','960x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],stdin=subprocess.PIPE);chapters=[];start=0
for b,h in zip(bare['states'],helmet['states']):
 assert b['frameDurationsMs']==h['frameDurationsMs'];ends=np.cumsum(b['frameDurationsMs']);total=float(ends[-1]);chapters.append({'state':b['id'],'startMs':start,'durationMs':total});start+=total
 pairs=[(Image.open(R/x.removeprefix('res://')).convert('RGBA'),Image.open(R/y.removeprefix('res://')).convert('RGBA')) for x,y in zip(b['frameFiles'],h['frameFiles'])]
 for tick in range(math.ceil(total*60/1000)):
  i=min(int(np.searchsorted(ends,tick*1000/60,side='right')),len(pairs)-1);board=Image.new('RGB',(960,600),'#242c31');d=ImageDraw.Draw(board);d.text((20,15),'KRUSHER DOM / INSPECTION / '+b['id'],font=font,fill='white')
  for j,im in enumerate(pairs[i]):
   full=im.resize((368,368),Image.Resampling.BILINEAR);board.paste(full,(25+j*470,70),full);small=im.resize((92,92),Image.Resampling.BILINEAR);board.paste(small,(170+j*470,460),small)
  d.text((20,565),'Six second source loop / bare and sealed / original inspection holds',font=font,fill='#cadcde');proc.stdin.write(board.tobytes())
proc.stdin.close();assert proc.wait()==0
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(video)]));duration=float(probe['format']['duration']);assert abs(duration-start/1000)<=1/60+0.001
(O/'preview.json').write_text(json.dumps({'durationSeconds':duration,'chapters':chapters,'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'scope':'Full canonical source pose chronology with original6000ms inspection holds; source-derived preview, not native recording. Separate native fixture checks1146pose selections and ordinary loops.'},indent=2))
(O/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{max-width:1000px;background:#242c31;color:white;font:18px system-ui;margin:24px auto;padding:0 16px}video{width:100%}a{color:#93c3c6}</style><h1>Krusher Dom / inspection</h1><video src="inspection-preview.mp4" controls playsinline loop></video><p><a href="inspection-preview.mp4">Open video directly</a></p><p>Four-direction bare/sealed inspection loops. All source poses, original6000ms holds. Source-derived review; separate native checks verify engine selection and looping. Complete animation goal remains active.</p>')
print(json.dumps({'videoSeconds':duration,'bytes':video.stat().st_size,'chapters':len(chapters)}))
