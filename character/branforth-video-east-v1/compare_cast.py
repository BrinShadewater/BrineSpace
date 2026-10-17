from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
specs=[('Bill',P.parent/'bill-video-east-v1/manifest.json'),('Veld',P.parent/'veld-runtime-walk-v1/manifest.json'),('Branforth',P/'manifest.json')]
clips=[]
for name,path in specs:
 m=json.loads(path.read_text());e=next(s for s in m['states'] if s['id']=='walk-east');clips.append((name,[Image.open(path.parent/f).convert('RGBA') for f in e['frameFiles']],e['frameDurationsMs']))
out=[]
for i in range(144):
 bg=Image.new('RGB',(1104,450),'#263139');d=ImageDraw.Draw(bg)
 for col,(name,frames,durations) in enumerate(clips):
  t=(i*1000/24)%sum(durations);n=0
  while n<len(durations)-1 and t>=durations[n]:t-=durations[n];n+=1
  big=frames[n].resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(col*368,25),big);small=frames[n].resize((64,64),Image.Resampling.LANCZOS);bg.paste(small,(col*368+152,384),small);d.text((col*368+10,7),name+' / '+str(round(sum(durations)))+' ms cycle',fill='white')
 out.append(bg)
out[0].save(P/'cast-east-review.gif',save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
