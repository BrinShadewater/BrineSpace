from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib

P = Path(__file__).resolve().parent
R = P.parents[1]
d = json.loads((P/'validate-evidence.json').read_text())
# Fixed viewport crops around the actual stationary foot, including doorway sparks.
# These do not recenter individual source poses or alter sprite pixels.
feet = {'north': (565,300), 'east': (525,500), 'south': (565,461), 'west': (606,500)}
boards=[]; inventory=[]
for direction, (x,y) in feet.items():
    rows=[r for r in d['records'] if r['case']==direction and r['state'] in ['torch-draw','weld','torch-stow']]
    unique = list({r['capture']:r for r in reversed(rows)}.values())[::-1]
    def crop(row):
        path=R/row['capture'].removeprefix('res://')
        return Image.open(path).convert('RGB').crop((x-90,y-130,x+90,y+30))
    for page in range((len(unique)+47)//48):
        board=Image.new('RGB',(1080,8*180),'#303b40'); draw=ImageDraw.Draw(board)
        for j,row in enumerate(unique[page*48:(page+1)*48]):
            at=(j%6*180,j//6*180)
            board.paste(crop(row),(at[0],at[1]+20))
            draw.text((at[0]+3,at[1]+3),row['state']+' '+str(row['index']),fill='white')
            path=R/row['capture'].removeprefix('res://')
            inventory.append({'capture':row['capture'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'key':row['key'],'index':row['index'],'sourceHash':row['sourceHash']})
        name=f'{direction}-page{page}.png';board.save(P/name);boards.append(name)
    # Repeated source slots reuse first-captured lighting/spark views; source clock is actual.
    frames=[]; durations=[]
    for i,row in enumerate(rows):
        im=Image.new('RGB',(360,340),'#303b40')
        im.paste(crop(row).resize((360,320),Image.Resampling.NEAREST),(0,20))
        ImageDraw.Draw(im).text((6,4),direction+' / '+row['state']+' / actual work clock',fill='white')
        next_time=rows[i+1]['time'] if i+1<len(rows) else row['time']+1/60
        frames.append(im);durations.append(max(10,round((next_time-row['time'])*1000)))
    frames[0].save(P/f'{direction}-work-clock.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0,disposal=2)
report={'boards':boards,'uniqueWorkCaptures':len(inventory),'inventory':inventory,'fixedViewportFeet':feet,'scope':'All distinct captured torch sources during four actual paid construction jobs. Native 1600x900 viewport crops, fixed per job. GIF follows recorded simulation source intervals and reuses first capture for repeated sources, so overlay flicker is not a continuous gameplay recording. Pixel bounds include tool/flame; no body-height normalization.'}
(P/'review-evidence.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'boards':boards,'uniqueWorkCaptures':len(inventory)}))
