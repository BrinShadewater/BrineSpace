from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-bunk-body-continue-v1'
result=json.loads((O/'validation.json').read_text());assert result['passed']
board=Image.new('RGB',(1040,2240),'#202a30');d=ImageDraw.Draw(board)
for g,gear in enumerate(['bare','helmet']):
    for phase in ['lower','held','rise','death']:
        row=g*4+['lower','held','rise','death'].index(phase)
        for col,side in enumerate(['before','after']):
            name=f'{gear}-{phase}-{side}'
            im=Image.open(O/f'{name}-room.png').convert('RGB').crop((330,330,590,580))
            board.paste(im,(col*520,row*280+30));d.text((col*520+8,row*280+8),name,fill='white')
            source=Image.open(O/f'{name}-source.png').convert('RGBA')
            board.paste(source,(col*520+260,row*280+8),source)
board.save(P/'native-fresh-continue.png')
print('16 native views paired with exact restored source poses')
