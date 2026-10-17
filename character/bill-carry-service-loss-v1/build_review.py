from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-service-loss-v1'
d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed'] and not d['failures'] and len(d['records'])==6
for gear in ['bare','helmet']:
 rows=[r for r in d['records'] if r['helmet']==(gear=='helmet')];board=Image.new('RGB',(600,720),'#22343e');draw=ImageDraw.Draw(board)
 for row,r in enumerate(rows):
  x=255+(r['foot'][0]-7680)*398/384;y=287+(r['foot'][1]-8064)*398/384
  for col,phase in enumerate(['before','after']):
   a=Image.open(O/(r['name']+'-'+phase+'-room.png')).convert('RGB');board.paste(a.crop((round(x)-75,round(y)-130,round(x)+75,round(y)+50)),(col*300,row*240+30))
   a=Image.open(O/(r['name']+'-'+phase+'-source.png')).convert('RGBA');assert a.width in [184,256];pivot=(128,224) if a.width==256 else (92,172);scale=82/148
   a=a.resize((round(a.width*scale),round(a.height*scale)),Image.Resampling.LANCZOS);board.paste(a,(round(col*300+225-pivot[0]*scale),round(row*240+180-pivot[1]*scale)),a)
   draw.text((col*300+5,row*240+5),str(r['sample'])+'s '+phase,fill='#dde8e9');draw.text((col*300+5,row*240+214),'ROOM / SOURCE82 '+(r['afterState'] if phase=='after' else 'carry'),fill='#dde8e9')
 board.save(P/(gear+'-service-loss.png'))
print('Six room/source pairs at common82/148 ruler with native pivots')
