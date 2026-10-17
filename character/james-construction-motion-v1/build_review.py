from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
P=Path(__file__).resolve().parent;R=P.parents[1]
feet={'north':(565,300),'east':(765,500),'south':(565,700),'west':(366,500)}
boards=[];counts={};allrecords=[]
for direction,(x,y) in feet.items():
    d=json.loads((P/direction/'evidence.json').read_text());rows=d['records'];counts[direction]=len(rows);allrecords+=rows
    def crop(row):return Image.open(R/row['capture'].removeprefix('res://')).convert('RGB').crop((x-90,y-130,x+90,y+30))
    for page in range(math.ceil(len(rows)/48)):
        subset=rows[page*48:(page+1)*48];board=Image.new('RGB',(1080,math.ceil(len(subset)/6)*180),'#303b40');draw=ImageDraw.Draw(board)
        for i,row in enumerate(subset):
            at=(i%6*180,i//6*180);board.paste(crop(row),(at[0],at[1]+20))
            draw.text((at[0]+3,at[1]+3),row['label'].removeprefix(direction+'-').replace('torch-','')+' '+row['phase']+' '+str(row['index']),fill='white')
        name=f'{direction}-page{page}.png';board.save(P/name);boards.append(name)
    sample=[r for r in rows if r['label']==direction+'-weld-power'];gif=[]
    for row in sample:
        im=Image.new('RGB',(360,344),'#303b40');im.paste(crop(row).resize((360,320),Image.Resampling.NEAREST),(0,24))
        ImageDraw.Draw(im).text((4,4),direction+' '+row['phase']+' / native pose sequence',fill='white');gif.append(im)
    gif[0].save(P/(direction+'-native-source-order.gif'),save_all=True,append_images=gif[1:],duration=50,loop=0,disposal=2)
evidence={'boards':boards,'counts':counts,'captures':len(allrecords),'scope':'Every native source-change capture from 24 actual controller power/door exit/hold/return cases and four repeated power losses mid-return. Fixed viewport crop per job; source-order GIF simplifies timing to50ms per captured pose, not a continuous gameplay recording. Room lighting/sparks change independently of original whole source material.','files':[{'path':r['capture'],'sha256':hashlib.sha256((R/r['capture'].removeprefix('res://')).read_bytes()).hexdigest()} for r in allrecords]}
(P/'review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
continued=P/'continue-evidence.json'
if continued.exists():
    c=json.loads(continued.read_text());board=Image.new('RGB',(1260,540),'#303b40');draw=ImageDraw.Draw(board)
    for i,row in enumerate(c['records']):
        direction=row['label'].split('-')[0];x,y={'north':(565,300),'east':(525,500),'south':(565,461)}[direction]
        if direction=='north' and not row['label'].endswith('-before'):y=542
        crop=Image.open(R/row['capture'].removeprefix('res://')).convert('RGB').crop((x-90,y-130,x+90,y+30))
        at=(i%7*180,i//7*180);board.paste(crop,(at[0],at[1]+20));draw.text((at[0]+3,at[1]+3),row['label'],fill='white')
    board.save(P/'continue-review.png')
print(json.dumps({'boards':boards,'captures':len(allrecords)}))
