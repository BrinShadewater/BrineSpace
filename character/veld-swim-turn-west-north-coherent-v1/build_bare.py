"""Package authored fixed-ruler yaw with exact selected swim endpoints."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
frames=[Image.open(R/'character/veld-water-west-coherent-v1/frames/bare/swim-west/000.png').convert('RGBA')]+[Image.open(H/f'graded-trials/{i:03}.png').convert('RGBA') for i in range(4)]+[Image.open(R/'character/veld-water-north-coherent-v1/frames/bare/swim-north/000.png').convert('RGBA')]
cov=json.loads((R/'character/veld-consistency-audit-v3/coverage.json').read_text());states=[];checks=0
for direction,row in [('west-north',frames),('north-west',list(reversed(frames)))]:
 key='swim-turn-'+direction;old=json.loads((R/cov['selected']['bare'][key]['manifest']).read_text());state=next(s for s in old['states'] if s['id']==key).copy();files=[]
 for i,im in enumerate(row):
  a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
  f=f'frames/bare/{key}/{i:03}.png';(H/f).parent.mkdir(parents=True,exist_ok=True);im.save(H/f);files.append(f)
 state['frameFiles']=files;states.append(state)
m=json.loads((R/'character/veld-water-west-coherent-v1/bare-manifest.json').read_text());m.update(name='Veld coherent west north ordinary swim turns bare',states=states,status='staged_bare_pending_helmet_native_world_review');(H/'bare-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
board=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(board)
for i,im in enumerate(frames):
 board.alpha_composite(im,(i*256,24));board.alpha_composite(im.resize((142,142),Image.Resampling.LANCZOS),(i*256+57,304));board.alpha_composite(im.resize((93,93),Image.Resampling.LANCZOS),(i*256+82,459));draw.text((i*256+4,4),str(i)+(' selected loop' if i in [0,5] else ' authored yaw'),fill='white')
board.save(H/'bare-turn-contact-v1.png');(H/'bare-fit-v1.json').write_text(json.dumps(dict(checks=checks,failures=0,exactEndpointPixels=True,installed=False),indent=2)+'\n');print(f'{checks} border checks PASS;2 bare states12refs staged')
