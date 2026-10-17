from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
clips=[]
for direction,folder in [('south','bill-video-south-v2'),('east','bill-video-east-v1'),('north','bill-video-north-v1'),('west','bill-video-west-v1')]:
 root=P.parent/folder;m=json.loads((root/'manifest.json').read_text());s=m['states'][0]
 clips.append((direction,[Image.open(root/f).convert('RGBA') for f in s['frameFiles']],s['frameDurationsMs']))
out=[]
for tick in range(144):
 bg=Image.new('RGB',(736,860),'#263139');d=ImageDraw.Draw(bg)
 for j,(direction,frames,durations) in enumerate(clips):
  t=(tick*1000/24)%sum(durations);n=0
  while n<len(durations)-1 and t>=durations[n]:t-=durations[n];n+=1
  x=j%2*368;y=j//2*430;d.text((x+12,y+8),f'BILL {direction.upper()} / SOURCE SPEED',fill='white')
  im=frames[n].resize((368,368),Image.Resampling.NEAREST);bg.paste(im,(x,y+25),im)
  tiny=frames[n].resize((64,64),Image.Resampling.LANCZOS);bg.paste(tiny,(x+152,y+360),tiny)
 out.append(bg)
out[0].save(P/'four-direction-review.gif',save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
