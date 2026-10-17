from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;old=P.parent/'james-water-north-v1'
packs={(tag,mode):json.loads(((P if tag=='new' else old)/(mode+'-manifest.json')).read_text()) for tag in ['old','new'] for mode in ['bare','helmet']}
frames=[];durations=[]
for action in ['tread','swim-start','swim-stop']:
    for slot in range(6):
        board=Image.new('RGB',(680,290),'#303b40');draw=ImageDraw.Draw(board)
        for row,mode in enumerate(['bare','helmet']):
            for col,tag in enumerate(['old','new']):
                pack=packs[tag,mode];s=next(s for s in pack['states'] if s['id']==action+'-north');root=P if tag=='new' else old
                im=Image.open(root/s['frameFiles'][slot]).convert('RGBA');small=im.resize((142,153),Image.Resampling.LANCZOS);at=(col*340+80,row*140+25);board.paste(small,at,small)
                draw.text((col*340+12,row*140+8),tag+' '+mode+' '+action+' '+str(slot),fill='white')
        frames.append(board);durations.append(int(next(s for s in packs['new','bare']['states'] if s['id']==action+'-north')['frameDurationsMs'][slot]))
frames[0].save(P/'comparison.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2,optimize=False)
frames[9].save(P/'comparison-midpoint.png')
print('Fixed82px old/new paired comparison, existing clocks')
