from pathlib import Path
import json,math,subprocess,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;R=P.parent.parent;B=R/'character/krusher-tablet-north-v2'
m=json.loads((P/'helmet-manifest.json').read_text());bare={s['id']:s for s in json.loads((B/'bare-manifest.json').read_text())['states']}
font=lambda n:ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),n)
video=P/'review/motion-preview.mp4'
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','800x600','-framerate','60','-i','-','-an','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',str(video)],stdin=subprocess.PIPE)
clock=0;chapters=[]
for state in m['states']:
 key=state['id'];ends=np.cumsum(state['frameDurationsMs']);chapters.append({'state':key,'sourceStartMs':clock,'sourceDurationMs':float(ends[-1])})
 for j in range(math.ceil(ends[-1]*60/1000)):
  i=min(int(np.searchsorted(ends,j*1000/60,side='right')),len(ends)-1)
  sheet=Image.new('RGB',(800,600),'#272b2e');d=ImageDraw.Draw(sheet);d.text((20,12),'KRUSHER / NORTH TABLET ACTION / HELMET FIT',font=font(29),fill='white')
  for col,(title,path) in enumerate([('Bare candidate',B/bare[key]['frameFiles'][i]),('Helmet face-fit study',P/state['frameFiles'][i])]):
   image=Image.open(path).convert('RGBA');d.text((25+col*390,52),title,font=font(23),fill='white');tile=image.resize((368,368),Image.Resampling.NEAREST);sheet.paste(tile,(10+col*390,83),tile);small=image.resize((92,92),Image.Resampling.LANCZOS);sheet.paste(small,(150+col*390,453),small)
  d.text((20,557),key+' / original gear shell and clock / unselected',font=font(22),fill='#bdcdd0');proc.stdin.write(sheet.tobytes())
 clock+=float(ends[-1])
proc.stdin.close();assert proc.wait()==0
(P/'review/preview.json').write_text(json.dumps({'chapters':chapters,'sourceDurationMs':clock,'videoHash':hashlib.sha256(video.read_bytes()).hexdigest(),'scope':'Source-derived 60fps paired preview; not native continuous capture'},indent=2)+'\n')
print(json.dumps({'videoBytes':video.stat().st_size,'sourceDurationMs':clock}))
