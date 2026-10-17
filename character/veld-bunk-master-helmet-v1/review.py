from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-bunk-master-helmet-v1'
for rotation in range(4):
    board=Image.new('RGB',(1820,1120),'#202a30');draw=ImageDraw.Draw(board)
    for g,gear in enumerate(['bare','helmet']):
        for s,stage in enumerate(['life_lie','life_get_up']):
            y=(g*2+s)*280
            for pose in range(7):
                im=Image.open(O/f'rotation{rotation}-{gear}-{stage}-pose{pose}-room.png').convert('RGB').crop((330,330,590,580))
                board.paste(im,(pose*260,y+30));draw.text((pose*260+6,y+8),f'R{rotation} {gear} '+('Lowering' if stage=='life_lie' else 'Rising')+f' {pose+1}',fill='white')
    board.save(P/f'native-motion-rotation{rotation}.png')
reg=json.loads((P/'package-checks.json').read_text());board=Image.new('RGB',(1792,280),'#202a30');draw=ImageDraw.Draw(board)
for i,(x,y) in enumerate(reg['positions']):
    im=Image.open(P/f'frames/helmet/bunk-enter-east/{i:03}.png').convert('RGBA');crop=im.crop((x-12,y-8,x+52,y+56)).resize((256,256),Image.Resampling.NEAREST);board.paste(crop,(i*256,24),crop);draw.text((i*256+8,4),f'pose{i},same4x ruler',fill='white')
board.save(P/'head-collar-review.png')
print('112unmodified native room crops on4motion boards;7same-ruler head crops')
