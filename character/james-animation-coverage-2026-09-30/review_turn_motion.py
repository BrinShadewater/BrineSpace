from pathlib import Path
import json
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
R=P.parents[1]
coverage=json.loads((P/'runtime-coverage.json').read_text())
out=P/'turn-height-review'
out.mkdir(exist_ok=True)
def state(mode,key):
    file=R/coverage['body' if mode=='bare' else 'equipment'][key]['path']
    m=json.loads(file.read_text())
    return file.parent,m,next(s for s in m['states'] if s['id']==key)
def draw_frame(board,mode,key,index,x,y):
    folder,m,s=state(mode,key)
    im=Image.open(folder/s['frameFiles'][index]).convert('RGBA')
    sc=82/m['standingHeight']
    im=im.resize((round(im.width*sc),round(im.height*sc)),Image.Resampling.BILINEAR)
    board.paste(im,(round(x-m['pivot'][0]*sc),round(y-m['pivot'][1]*sc)),im)
keys=['carry-turn-east-west','carry-turn-north-south']
frames=[]
for i in range(11):
    board=Image.new('RGB',(960,420),'#303b40')
    d=ImageDraw.Draw(board)
    d.text((12,10),'James dry carrying turns / current selected PNGs / 82px standing scale / original 1600ms clocks',fill='white')
    for row,key in enumerate(keys):
        start,end=key.split('-')[-2:]
        y=70+row*175
        d.text((12,y-26),key+' / pose '+str(i),fill='white')
        for mode,shift in [('bare',0),('helmet',110)]:
            for kind,k,index,x in [('start','idle-'+start,0,70),('turn',key,i,410),('end','idle-'+end,0,750)]:
                draw_frame(board,mode,k,index,x+shift,y+105)
                d.text((x+shift-40,y-5),kind+' '+mode,fill='white')
    frames.append(board)
_,_,s=state('bare',keys[0])
assert all(state(mode,key)[2]['frameDurationsMs']==s['frameDurationsMs'] for key in keys for mode in ['bare','helmet'])
frames[0].save(out/'dry-half-turn-masters.gif',save_all=True,append_images=frames[1:],duration=s['frameDurationsMs'],loop=0)
frames[5].save(out/'dry-half-turn-masters-midpoint.png')
print('Two dry half turns compared against stationary start/end masters; selected 1600ms clocks')
