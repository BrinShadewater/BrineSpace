from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
modes={mode:json.loads((P/(mode+'-manifest.json')).read_text()) for mode in ['bare','helmet']}
frames=[];durations=[]
for state in modes['bare']['states']:
    key=state['id']
    for index in range(6):
        board=Image.new('RGB',(1140,345),'#303b40');d=ImageDraw.Draw(board)
        d.text((8,8),'James North rest polish / '+key+' / bare + shared helmet / 82px / 54px / 27px',fill='white')
        for mode,offset in [('bare',0),('helmet',256)]:
            s=next(s for s in modes[mode]['states'] if s['id']==key)
            im=Image.open(P/s['frameFiles'][index]).convert('RGBA');board.paste(im,(offset,38),im)
            for height,x in [(82,525),(54,810),(27,1025)]:
                sc=height/148;small=im.resize((round(256*sc),round(256*sc)),Image.Resampling.BILINEAR)
                base=x+(0 if mode=='bare' else round(256*sc)+4)
                board.paste(small,(base,294-round(224*sc)),small)
        frames.append(board);durations.append(state['frameDurationsMs'][index])
frames[0].save(P/'review.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
frames[8].save(P/'review-midpoint.png')
print('Paired3-state review, original selected clocks, fixed148px physical size')
