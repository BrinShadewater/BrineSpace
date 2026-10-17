from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];O=R/'output/veld-workshop-west-stop-route-v3'
d=json.loads((O/'journeys.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed']
evidence={'validation':v,'scope':'Chronological native/source stop joins, both gears; not full continuous cadence or production interruption acceptance','boards':[]}
for journey in d['journeys']:
 if not journey['candidate']:continue
 records=journey['records'];stops=[r for r in records if r['key']=='carry-stop-phase2-west'];assert stops
 selected=[next(r for r in reversed(records) if r['step']<stops[0]['step'] and r.get('capture'))]
 for slot in range(4):selected.append(next(r for r in stops if r['slot']==slot and r.get('capture')))
 selected.append(next(r for r in records if r['step']>stops[-1]['step'] and r['key']=='carry-turn-west-north' and r.get('capture')))
 board=Image.new('RGB',(1320,680),'#202a30');draw=ImageDraw.Draw(board)
 for n,row in enumerate(selected):
  x=n%3*440;y=n//3*340
  native=Image.open(O/(row['capture']+'-native.png')).convert('RGB');native.thumbnail((430,260));board.paste(native,(x,y+24))
  source=Image.new('RGBA',(256,256),'#202a30');source.alpha_composite(Image.open(O/(row['capture']+'-source.png')).convert('RGBA'));source=source.resize((100,100),Image.Resampling.NEAREST);board.paste(source.convert('RGB'),(x+330,y+230))
  draw.text((x+5,y+5),row['key']+' pose '+str(row['slot']),fill='white')
 gear='helmet' if journey['helmet'] else 'bare';out=P/(gear+'-stop-world-review.png');board.save(out);evidence['boards'].append({'file':out.name,'pairs':len(selected),'captures':[r['capture'] for r in selected]})
(P/'world-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print(json.dumps(evidence))
