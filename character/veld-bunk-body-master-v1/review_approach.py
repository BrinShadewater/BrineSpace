from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-bunk-body-approach-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text())
for r in records:
    gear=r['gear'];n=r['captures'];cols=5;rows=(n+cols-1)//cols
    board=Image.new('RGB',(1300,rows*280),'#202a30');d=ImageDraw.Draw(board)
    for i in range(n):
        # Initial release stands left of room centre; preserve the whole figure.
        box=(260,330,520,580) if i==0 else (330,330,590,580)
        im=Image.open(O/f'{gear}-pose-{i:02}-room.png').convert('RGB').crop(box);x=i%5*260;y=i//5*280
        board.paste(im,(x,y+30));d.text((x+6,y+6),f'{gear} actual approach/rest {i+1}',fill='white')
    board.save(P/f'native-approach-{gear}.png')
    board=Image.new('RGB',(1536,((n+5)//6)*292),'#202a30');d=ImageDraw.Draw(board)
    for i in range(n):
        im=Image.open(O/f'{gear}-pose-{i:02}-source.png').convert('RGBA');x=i%6*256;y=i//6*292
        assert im.size in [(184,184),(256,272)]
        pos=(36,52) if im.size==(184,184) else (0,0)
        board.paste(im,(x+pos[0],y+18+pos[1]),im);d.text((x+6,y+2),f'actual source {i+1} / same ruler',fill='white')
    board.save(P/f'approach-source-{gear}.png')
print('Paired actual approach/rest native boards and same-ruler source boards')
