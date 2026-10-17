from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;O=P.parents[1]/'output/veld-bunk-body-emergency-v1'
assert json.loads((O/'validation.json').read_text())['passed']
records=json.loads((O/'records.json').read_text())
def pad(source):
    im=Image.open(source).convert('RGBA')
    if im.size==(184,184):
        full=Image.new('RGBA',(256,272));full.alpha_composite(im,(36,52));return full
    return im
for gear in ['bare','helmet']:
    for phase in ['lower-0.81','held','rise-0.9']:
        name=f'{gear}-fire-{phase}';record=next(r for r in records if r['name']==name)
        changes=[s for s in record['samples'] if 'rendered' in s]
        board=Image.new('RGB',(920,(len(changes)+1)*300),'#202a30');draw=ImageDraw.Draw(board)
        gif=[];durations=[]
        for row,sample in enumerate(changes):
            source=pad(O/f'{name}-slot-{row:02d}-source.png')
            native=Image.open(O/f'{name}-slot-{row:02d}-room.png').convert('RGB').crop((253,285,653,585))
            board.paste(native,(0,row*300));board.paste(source,(400,row*300),source)
            draw.text((680,row*300+8),f"{sample['stage'] or 'upright'}\n{sample['tick']*20}ms",fill='white')
            gif.append(source)
            end=changes[row+1]['tick'] if row+1<len(changes) else sample['tick']+5
            durations.append((end-sample['tick'])*60)
        row=len(changes)
        refuge=Image.open(O/f'{name}-refuge-room.png').convert('RGB').crop((245,275,665,695))
        board.paste(refuge.resize((300,300)),(0,row*300))
        source=pad(O/f'{name}-refuge-source.png');board.paste(source,(400,row*300),source)
        draw.text((680,row*300+8),'Actual refuge\n'+record['escapedCell'],fill='white')
        board.save(P/f'native-emergency-{gear}-{phase}.png')
        gif[0].save(P/f'emergency-{gear}-{phase}.gif',save_all=True,append_images=gif[1:],duration=durations,disposal=2,loop=0)
    for phase in ['lower-0.81','held','rise-0.9']:
        names=[f'{gear}-gear-{phase}-{side}' for side in ['before','after']]
        names+=[f'{gear}-extinguished-{phase}-{side}' for side in ['before','after','upright']]
        board=Image.new('RGB',(720,len(names)*300),'#202a30');draw=ImageDraw.Draw(board)
        for row,name in enumerate(names):
            im=Image.open(O/f'{name}-room.png').convert('RGB').crop((253,285,653,585));board.paste(im,(0,row*300))
            source=pad(O/f'{name}-source.png');board.paste(source,(400,row*300),source);draw.text((405,row*300+4),name,fill='white')
        board.save(P/f'native-emergency-contexts-{gear}-{phase}.png')
print('Six finite fire-rise/native refuge boards and six gear/extinguished boards; original source pivots preserved')
