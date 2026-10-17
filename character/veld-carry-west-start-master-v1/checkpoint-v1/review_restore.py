from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[2];C=R/'output/veld-workshop-motion-checkpoints-v2';O=R/'output/veld-workshop-motion-restore-v2'
validation=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert validation['passed']
rest=json.loads((O/'restore-review.json').read_text(encoding='utf-8'));routes=json.loads((C/'journeys.json').read_text(encoding='utf-8'))
evidence={'validation':validation,'scope':'Ten fresh restored native poses versus their uninterrupted real-route native/source observations; exact pixel/clock and60tick progress assertions in engine','boards':[]}
labels={'carry-held-east':'Holding East','carry-turn-east-west':'Turning East to West','carry-start-west':'First step West','carry-stop-phase2-west':'Stopping West','carry-turn-west-north':'Turning West to North'}
slots={'carry-held-east':0,'carry-turn-east-west':3,'carry-start-west':1,'carry-stop-phase2-west':2,'carry-turn-west-north':3}
for helmet in [False,True]:
 rows=[x for x in rest['results'] if x['gear']==helmet];board=Image.new('RGB',(1320,350*len(rows)),'#202a30');draw=ImageDraw.Draw(board);observations=[]
 journey=next(j for j in routes['journeys'] if j['candidate'] and j['helmet']==helmet)
 for index,row in enumerate(rows):
  original=next(r for r in journey['records'] if r['key']==row['key'] and r['slot']==slots[row['key']] and r.get('capture'))
  draw.text((10,index*350+5),labels[row['key']]+' | Original / Restored / Master source',fill='white')
  for x,path in [(0,C/(original['capture']+'-native.png')),(520,O/(row['capture']+'-native.png'))]:
   im=Image.open(path).convert('RGB');im.thumbnail((510,310));board.paste(im,(x,index*350+30))
  im=Image.new('RGBA',(256,256),'#202a30');im.alpha_composite(Image.open(O/(row['capture']+'-source.png')).convert('RGBA'));board.paste(im.convert('RGB'),(1050,index*350+30))
  observations.append({'key':row['key'],'original':original['capture'],'restored':row['capture'],'comparisonTicks':row['comparisonTicks']})
 gear='helmet' if helmet else 'bare';out=P/(gear+'-checkpoint-review.png');board.save(out);evidence['boards'].append({'file':out.name,'observations':observations})
(P/'restore-review-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8');print(json.dumps({'boards':len(evidence['boards']),'restoredComparisons':len(rest['results']),'checks':rest['checks'],'failures':rest['failures']}))
