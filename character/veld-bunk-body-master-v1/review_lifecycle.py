from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-bunk-body-lifecycle-v1'
report=json.loads((O/'validation.json').read_text());assert report['passed']
records=json.loads((O/'records.json').read_text())
for record in records:
    if 'cycle' not in record:continue
    gear=record['gear'];n=record['capturedSlots'];cols=5;rows=(n+cols-1)//cols
    board=Image.new('RGB',(1300,rows*280),'#202a30');d=ImageDraw.Draw(board)
    for i in range(n):
        im=Image.open(O/f'{gear}-cycle-{i:02}-room.png').convert('RGB').crop((330,330,590,580));x=i%cols*260;y=i//cols*280
        board.paste(im,(x,y+30));d.text((x+8,y+8),f'{gear} actual cycle pose {i+1}',fill='white')
    board.save(P/f'native-cycle-{gear}.png')
board=Image.new('RGB',(1040,1120),'#202a30');d=ImageDraw.Draw(board)
for gear_index,gear in enumerate(['bare','helmet']):
    for loss_index,loss in enumerate(['power','suspended']):
        y=(gear_index*2+loss_index)*280
        for phase_index,elapsed in enumerate(['0.81','2.0']):
            for side_index,side in enumerate(['before','after']):
                name=f'{gear}-{loss}-{elapsed}-{side}'
                im=Image.open(O/f'{name}-room.png').convert('RGB').crop((330,330,590,580));x=(phase_index*2+side_index)*260
                board.paste(im,(x,y+30));d.text((x+6,y+8),name,fill='white')
board.save(P/'native-service-interruptions.png')
print('Complete native pose sequences in both gears;16 actual service interruption views')
