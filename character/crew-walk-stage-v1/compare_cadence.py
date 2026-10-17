from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;directions=['south','east','north','west'];clips={};proposals=[]
for who in ['bill','veld','branforth']:
 root=P.parent/'veld-runtime-walk-v1' if who=='veld' else P/who
 m=json.loads((root/'manifest.json').read_text())
 for s in m['states']:
  if not s['id'].startswith('walk-'):continue
  frames=[Image.open(root/f).convert('RGBA') for f in s['frameFiles']];cycles=s.get('gaitCycles',1);duration=1500*cycles
  clips[(who,s['id'][5:])]=(frames,duration)
  proposals.append(dict(character=who,state=s['id'],gaitCycles=cycles,originalDurationMs=sum(s['frameDurationsMs']),proposedDurationMs=duration,frameDurationsMs=[round((n+1)*duration/len(frames))-round(n*duration/len(frames)) for n in range(len(frames))]))
out=[]
for tick in range(144):
 bg=Image.new('RGB',(828,1016),'#263139');draw=ImageDraw.Draw(bg)
 for col,who in enumerate(['bill','veld','branforth']):
  for row,direction in enumerate(directions):
   frames,duration=clips[(who,direction)];t=tick*1000/24;n=int((t%duration)/duration*len(frames));im=frames[n];x=col*276;y=row*254
   draw.text((x+8,y+5),f'{who.upper()} {direction.upper()} / 1.5s STRIDE',fill='white');large=im.resize((230,230),Image.Resampling.NEAREST);bg.paste(large,(x+8,y+22),large)
   small=im.resize((64,64),Image.Resampling.LANCZOS);bg.paste(small,(x+208,y+176),small)
 out.append(bg)
out[0].save(P/'matched-cadence-review.gif',save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
(P/'cadence-proposal.json').write_text(json.dumps(dict(status='Timing-only review proposal, not applied to manifests or runtime; no frame creation',clips=proposals),indent=2))
