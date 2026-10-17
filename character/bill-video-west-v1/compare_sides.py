from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;clips=[]
for direction,root in [('east',P.parent/'bill-video-east-v1'),('west',P)]:
 m=json.loads((root/'manifest.json').read_text());e=m['states'][0];clips.append((direction,[Image.open(root/f).convert('RGBA') for f in e['frameFiles']],e['frameDurationsMs']))
out=[]
for i in range(144):
 bg=Image.new('RGB',(736,445),'#263139');d=ImageDraw.Draw(bg)
 for col,(name,frames,durations) in enumerate(clips):
  t=(i*1000/24)%sum(durations);n=0
  while n<len(durations)-1 and t>=durations[n]:t-=durations[n];n+=1
  im=frames[n].resize((368,368),Image.Resampling.NEAREST);bg.paste(im,(368*col,25),im);im=frames[n].resize((64,64),Image.Resampling.LANCZOS);bg.paste(im,(col*368+152,380),im);d.text((col*368+10,7),'BILL '+name.upper()+' / SOURCE SPEED',fill='white')
 out.append(bg)
out[0].save(P/'east-west-review.gif',save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
