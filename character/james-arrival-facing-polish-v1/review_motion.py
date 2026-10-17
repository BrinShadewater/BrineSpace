"""Selected tablet PNGs at the verified six-second dry diagnostics window."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
c=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text())
clips={}
for mode in ['bare','helmet']:
    for facing in ['east','south','west','north']:
        key='interact-'+facing
        file=R/c['body' if mode=='bare' else 'equipment'][key]['path']
        m=json.loads(file.read_text());s=next(s for s in m['states'] if s['id']==key)
        clips[mode,facing]=(file.parent,m,s)
cache={};frames=[]
for elapsed in range(0,6000,40):
    board=Image.new('RGB',(960,510),'#303b40');draw=ImageDraw.Draw(board)
    draw.text((12,8),'James diagnostics / accepted selected sprites / 82px / full5.5s tablet cycle +0.5s neutral',fill='white')
    for row,facing in enumerate(['east','south','west','north']):
        for mode,x in [('bare',320),('helmet',660)]:
            folder,m,s=clips[mode,facing];cursor=elapsed;index=len(s['frameFiles'])-1
            for i,duration in enumerate(s['frameDurationsMs']):
                if cursor<duration:index=i;break
                cursor-=duration
            file=folder/s['frameFiles'][index]
            if file not in cache:
                im=Image.open(file).convert('RGBA');sc=82/m['standingHeight']
                cache[file]=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.BILINEAR)
            im=cache[file];sc=82/m['standingHeight'];y=130+row*120
            board.paste(im,(round(x-m['pivot'][0]*sc),round(y-m['pivot'][1]*sc)),im)
            draw.text((x-55,y-100),facing+' '+mode,fill='white')
    frames.append(board)
frames[0].save(P/'review.gif',save_all=True,append_images=frames[1:],duration=40,loop=0)
frames[75].save(P/'review-midpoint.png')
print('Four directional paired diagnostics at6s, sampled40ms, no art changes')
