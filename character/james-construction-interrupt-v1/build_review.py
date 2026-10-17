from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
d=json.loads((P/'validate-evidence.json').read_text());boards=[]
feet={'north':(565,300),'east':(525,500),'south':(565,461),'west':(606,500)}
for direction,(x,y) in feet.items():
    rows=[r for r in d['records'] if r['direction']==direction]
    board=Image.new('RGB',(540,1080),'#303b40');draw=ImageDraw.Draw(board)
    for i,row in enumerate(rows):
        im=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB').crop((x-90,y-130,x+90,y+30))
        at=(i%3*180,i//3*180);board.paste(im,(at[0],at[1]+20));draw.text((at[0]+3,at[1]+3),row['label'].removeprefix(direction+'-'),fill='white')
    name=direction+'-interruptions.png';board.save(P/name);boards.append(name)
(P/'review-evidence.json').write_text(json.dumps({'boards':boards,'records':len(d['records']),'scope':'Before/half-second-held/first-resumed native source in 24 power/door cases. Does not establish smooth transition motion.'},indent=2))
print(json.dumps({'boards':boards,'captures':len(d['records'])}))
continued=P/'continue-evidence.json'
if continued.exists():
    c=json.loads(continued.read_text());board=Image.new('RGB',(1260,540),'#303b40');draw=ImageDraw.Draw(board)
    for i,row in enumerate(c['records']):
        direction=row['label'].split('-')[0];x,y=feet[direction]
        # Fresh North scene restores a different camera scroll. One fixed crop
        # for all its post-restore poses; actor contact/source pixels remain exact.
        if direction=='north' and not row['label'].endswith('-before'):y=542
        im=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB').crop((x-90,y-130,x+90,y+30))
        at=(i%7*180,i//7*180);board.paste(im,(at[0],at[1]+20));draw.text((at[0]+3,at[1]+3),row['label'].replace('torch-',''),fill='white')
    board.save(P/'continue-review.png')
