from pathlib import Path
from PIL import Image,ImageDraw
import json,math,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'room-journey-v286';j=json.loads((o/'travel-trace.json').read_bytes());m=json.loads((o/'bare-manifest.json').read_bytes());clock=m['states'][0]['frameDurationsMs'];cycle=sum(clock)/1000.0;reports=[]
for route in j:
 samples=route['samples'];start=route['start'];seen=set();errors=[];distance=[]
 for row in samples:
  dist=math.dist(row['worldFoot'],start);distance.append(dist);expected=dist/route['strideWorldUnits']*cycle;errors.append(abs(row['playerPhase']-expected));seen.add(row['sourceIndex'])
 reports.append(dict(gear=route['gear'],samples=len(samples),sourceIndices=sorted(seen),travelWorldUnits=distance[-1],maxDistancePhaseErrorSeconds=max(errors),strideWorldUnits=route['strideWorldUnits'],scope='Actual NPC root/player distance coupling; physical foot landmarks not tracked.'))
(o/'travel-analysis.json').write_text(json.dumps(dict(routes=reports,physicalFootContactAccepted=False,normalChanged=False),indent=2)+'\n');print(json.dumps(reports))
for mode in ['bare','helmet']:
 labels=['entry-000','quarter','before-continue','after-continue','unload-entry','unload-held'];ims=[Image.open(o/f'arrival-captures/{mode}-{x}.png').convert('RGBA') for x in labels];cw=max(im.width for im in ims);ch=max(im.height for im in ims)+24;b=Image.new('RGBA',(cw*3,ch*2),(47,59,63,255));d=ImageDraw.Draw(b)
 for i,(label,im) in enumerate(zip(labels,ims)):
  x=(i%3)*cw;y=(i//3)*ch;b.alpha_composite(im,(x,y+24));d.text((x+4,y+4),mode+' '+label,fill='white')
 b.save(o/f'{mode}-room-review.png')
