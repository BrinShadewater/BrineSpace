from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];O=R/'output/veld-workshop-motion-clock-v1'
d=json.loads((O/'journeys.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed']
evidence={'validation':v,'scope':'Simulation-clocked turns/start/stop, native source pairs; no continuous cadence or full safety/checkpoint acceptance','boards':[]}
for journey in d['journeys']:
 if not journey['candidate']:continue
 records=journey['records'];stops=[r for r in records if r['key']=='carry-stop-phase2-west'];assert stops
 selected=[]
 for key in ['carry-turn-east-west','carry-start-west','carry-stop-phase2-west','carry-turn-west-north']:
  selected.extend(r for r in records if r['key']==key and r.get('capture'))
 board=Image.new('RGB',(1760,((len(selected)+3)//4)*340),'#202a30');draw=ImageDraw.Draw(board)
 for n,row in enumerate(selected):
  x=n%4*440;y=n//4*340
  native=Image.open(O/(row['capture']+'-native.png')).convert('RGB');native.thumbnail((430,260));board.paste(native,(x,y+24))
  source=Image.new('RGBA',(256,256),'#202a30');source.alpha_composite(Image.open(O/(row['capture']+'-source.png')).convert('RGBA'));source=source.resize((100,100),Image.Resampling.NEAREST);board.paste(source.convert('RGB'),(x+330,y+230))
  draw.text((x+5,y+5),row['key']+' pose '+str(row['slot']),fill='white')
 gear='helmet' if journey['helmet'] else 'bare';out=P/(gear+'-stop-world-review.png');board.save(out);evidence['boards'].append({'file':out.name,'pairs':len(selected),'captures':[r['capture'] for r in selected]})
(P/'world-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print(json.dumps(evidence))
