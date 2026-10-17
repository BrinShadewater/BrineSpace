from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text());s=m['states'][0]
frames=[Image.open(P/f).convert('RGBA') for f in s['frameFiles']]
master=Image.open(P/'master-standing.png').convert('RGBA')
out=[]
for tick in range(144):
    bg=Image.new('RGB',(828,330),'#263139');d=ImageDraw.Draw(bg)
    t=tick*1000/24
    picks=[master,frames[int((t%sum(s['frameDurationsMs']))/sum(s['frameDurationsMs'])*len(frames))],frames[int((t%1500)/1500*len(frames))]]
    for j,(im,title) in enumerate(zip(picks,['STANCE REFERENCE','SOURCE SPEED / 0.79s','TIMING PROPOSAL / 1.5s'])):
        x=j*276;d.text((x+8,8),title,fill='white');big=im.resize((276,276),Image.Resampling.NEAREST);bg.paste(big,(x,30),big)
        tiny=im.resize((64,64),Image.Resampling.LANCZOS);bg.paste(tiny,(x+208,250),tiny)
    out.append(bg)
out[0].save(P/'timing-review.gif',save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
(P/'timing-proposal.json').write_text(json.dumps(dict(appliedToManifest=False,cycleDurationMs=1500,sourceCycleDurationMs=sum(s['frameDurationsMs']),frameCount=len(frames),method='Playback timing only; no interpolation or additional poses'),indent=2))
print('Created master/source-speed/slower comparison; manifest retains original cadence.')
