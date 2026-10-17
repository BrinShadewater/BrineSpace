from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path(__file__).resolve().parent
e=json.loads((P/'evidence.json').read_bytes());assert e['complete'] and e['failures']==0
for case in e['cases']:
    records=[r for r in e['records'] if r['case']==case['id']]
    board=Image.new('RGB',(5*320,((len(records)+4)//5)*320),'#303b40');d=ImageDraw.Draw(board)
    for i,r in enumerate(records):
        x,y=map(round,r['footViewport']);im=Image.open(P.parents[1]/r['capture'].removeprefix('res://'))
        crop=im.crop((x-150,y-220,x+150,y+80));at=((i%5)*320,(i//5)*320+20)
        board.paste(crop,at);d.text((at[0],at[1]-18),r['stage']+' '+str(r['index'])+' '+str(round(r['timer'],2)),fill='white')
    board.save(P/(case['id']+'-native-review.png'))
print('Eight actual furniture contact/Continue sequence review boards created.')
