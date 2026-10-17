from pathlib import Path
import json
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text());checks=0
for variant in ['bare','helmet']:
 m=json.loads((H/f'{variant}-manifest.json').read_text());states={s['id']:s for s in m['states']}
 for field,expected in [('frameWidth',256),('frameHeight',256),('pivot',[128,128]),('standingHeight',148),('precomposed',True)]:assert m[field]==expected;checks+=1
 for key,state in states.items():
  src=json.loads((R/cov['selected'][variant][key]['manifest']).read_text());old=next(s for s in src['states'] if s['id']==key)
  for field in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']:assert state[field]==old[field];checks+=1
  assert m['strideDistanceCells']==src['strideDistanceCells'];checks+=1
  for file in state['frameFiles']:
   im=Image.open(H/file);assert im.size==(256,256) and im.mode=='RGBA';checks+=1
 for i in range(6):assert Image.open(H/states['swim-start-east']['frameFiles'][i]).tobytes()==Image.open(H/states['swim-stop-east']['frameFiles'][5-i]).tobytes();checks+=1
 for action,slot,loop in [('swim-start-east',0,'tread-east'),('swim-start-east',5,'swim-east'),('swim-stop-east',0,'swim-east'),('swim-stop-east',5,'tread-east')]:assert Image.open(H/states[action]['frameFiles'][slot]).tobytes()==Image.open(H/states[loop]['frameFiles'][0]).tobytes();checks+=1
(H/'packaging-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'scope':'paired loop/start/stop timing/medium/stride/geometry, exact endpoint joins and reverse stops','installed':False},indent=2)+'\n',encoding='utf-8');print(f'{checks} packaging/exact-join checks PASS.')
