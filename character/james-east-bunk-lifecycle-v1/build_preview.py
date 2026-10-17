from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
e=json.loads((P/'evidence.json').read_bytes());assert e['complete'] and e['failures']==0
groups=[[r for r in e['records'] if r['case']==mode+'-normal'] for mode in ['bare','helmet']]
assert len(groups[0])==len(groups[1])==16
frames=[];durations=[]
for i in range(16):
    board=Image.new('RGB',(600,330),'#303b40');draw=ImageDraw.Draw(board)
    for side,group in enumerate(groups):
        r=group[i];x,y=map(round,r['footViewport']);im=Image.open(R/r['capture'].removeprefix('res://'))
        board.paste(im.crop((x-150,y-220,x+150,y+80)),(side*300,30))
        draw.text((side*300+8,8),('Bare' if side==0 else 'Helmet')+' — captured bunk poses',fill='white')
    frames.append(board)
    durations.append(max(20,round((groups[0][i+1]['clock']-groups[0][i]['clock'])*1000/10)*10) if i<15 else 600)
frames[0].save(P/'paired-native-bunk-preview.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
(P/'preview-scope.json').write_text(json.dumps({'kind':'native captured source-change poses replayed at recorded actor-clock intervals, not continuous native video','posesPerGear':16,'durationMs':sum(durations)},indent=2))
print('Paired captured bunk pose preview saved:',sum(durations),'ms.')
