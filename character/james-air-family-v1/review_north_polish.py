from pathlib import Path
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
for mode in ['bare','helmet']:
    board=Image.new('RGB',(1320,360),'#303b40');draw=ImageDraw.Draw(board)
    for row,action in enumerate(['distress','recovery']):
        for i in range(6):
            label=mode+'-'+action+'-north-'+str(i).zfill(3);im=Image.open(P/'north-polish-captures'/(label+'.png')).convert('RGB');x,y=im.width//2,im.height//2;crop=im.crop((x-105,y-100,x+105,y+50));at=(i*220,row*180+25);board.paste(crop,at);draw.text((at[0]+3,row*180+3),label,fill='white')
    board.save(P/('native-north-polish-behaviour-'+mode+'.png'))
print('North polished actual-state capture boards;24 native captures')
