from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[2];O=R/'output/veld-workshop-north-rise-join-v3'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed']
d=json.loads((O/'journeys.json').read_text(encoding='utf-8'));reviews=[]
for j in d['journeys']:
 if not j['candidate']:continue
 gear='helmet' if j['helmet'] else 'bare';poses={};idle=None
 for x in j['records']:
  if not x.get('capture'):continue
  if x['key']=='unload-north':poses.setdefault(x['slot'],x['capture']+'-native.png')
  if x['key']=='idle-north':idle=x['capture']+'-native.png'
 assert len(poses)==7 and idle
 picks=[poses[i] for i in range(7)]+[idle]+[x['capture'] for x in j['departures']]
 board=Image.new('RGB',(1620,1470),'#202a30');draw=ImageDraw.Draw(board)
 for i,n in enumerate(picks):
  image=Image.open(O/n).convert('RGB').crop((250,220,655,693));x=i%4*405;y=i//4*490
  board.paste(image,(x,y+17));draw.text((x+3,y+2),n,fill='white')
 name=gear+'-world-rise-departure-review.png';board.save(P/name)
 reviews.append({'gear':gear,'board':name,'captures':picks,'sha256':[hashlib.sha256((O/n).read_bytes()).hexdigest() for n in picks],'departures':j['departures']})
(P/'world-review-evidence.json').write_text(json.dumps({'validation':v,'checks':d['checks'],'failures':d['failures'],'reviews':reviews,'visualReview':'pending','scope':'actual default workshop prescribed room/service route, authoring-only subclass/source/prop, both gears; contact/idle/departure samples not continuous cadence or production ownership/Continue acceptance'},indent=2)+'\n',encoding='utf-8')
print('22 native workshop pose/idle/departure views prepared.')
