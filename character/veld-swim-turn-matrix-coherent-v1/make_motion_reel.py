"""Full-speed paired twelve-direction review from exact selected PNG clocks."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
import imageio_ffmpeg
H=Path(__file__).resolve().parent;R=H.parents[1];tracks={};cache={}
def load(p):
    if p not in cache:cache[p]=Image.open(p).convert('RGBA')
    return cache[p]
for gear in ['bare','helmet']:
    m=json.loads((H/(gear+'-manifest.json')).read_text())
    for turn in m['states']:
        direction=turn['id'].removeprefix('swim-turn-');source,dest=direction.split('-');track=[]
        for d in [source,dest]:
            base=R/'character'/('veld-water-'+d+'-coherent-v1');loop=next(s for s in json.loads((base/(gear+'-manifest.json')).read_text())['states'] if s['id']=='swim-'+d)
            track.extend((base/p,t,loop['id'],i) for i,(p,t) in enumerate(zip(loop['frameFiles'],loop['frameDurationsMs'])))
            if d==source:track.extend((H/p,t,turn['id'],i) for i,(p,t) in enumerate(zip(turn['frameFiles'],turn['frameDurationsMs'])))
        track.append((base/loop['frameFiles'][0],1000,'destination hold',0));tracks.setdefault(direction,{})[gear]=track
for pair in tracks.values():assert [x[1] for x in pair['bare']]==[x[1] for x in pair['helmet']]
writer=imageio_ffmpeg.write_frames(str(H/'full-speed-paired-motion-v1.mp4'),(1536,1120),fps=50,codec='libx264',quality=8,pix_fmt_out='yuv420p',ffmpeg_log_level='error');writer.send(None)
for ms in range(0,4000,20):
    board=Image.new('RGBA',(1536,1120),'#202a30');draw=ImageDraw.Draw(board)
    for index,(direction,pair) in enumerate(tracks.items()):
        x=(index%3)*512;y=(index//3)*280
        for j,gear in enumerate(['bare','helmet']):
            elapsed=ms;chosen=pair[gear][-1]
            for frame in pair[gear]:
                if elapsed<frame[1]:chosen=frame;break
                elapsed-=frame[1]
            board.alpha_composite(load(chosen[0]),(x+j*256,y+24))
            draw.text((x+j*256+4,y+4),gear+' '+direction+' '+str(ms)+'ms /'+str(chosen[3]),fill='white')
    writer.send(np.array(board.convert('RGB')))
writer.close()
(H/'motion-reel-checks.json').write_text(json.dumps(dict(fps=50,seconds=4,directions=12,gearStates=24,pairedClocks=True,physicalStandingRuler=148,scope='Full-speed deterministic art/clock review; no world route or owner acceptance claim',manifestHashes={g:hashlib.sha256((H/(g+'-manifest.json')).read_bytes()).hexdigest() for g in ['bare','helmet']}),indent=2)+'\n')
print('Full-speed 4-second paired motion reel:12directions/24gearstates')
