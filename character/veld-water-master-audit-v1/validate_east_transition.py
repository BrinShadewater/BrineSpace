from pathlib import Path
import json
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];cov=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text());checks=0
for variant in ['bare','helmet']:
 m=json.loads((HERE/f'east-transition-{variant}-manifest.json').read_text());by={s['id']:s for s in m['states']};start=by['swim-start-east'];stop=by['swim-stop-east']
 for state in m['states']:
  source=json.loads((ROOT/cov['selected'][variant][state['id']]['manifest']).read_text());old=next(s for s in source['states'] if s['id']==state['id'])
  for field in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']:assert state[field]==old[field];checks+=1
  for field in ['frameWidth','frameHeight','pivot','standingHeight','precomposed','strideDistanceCells']:assert m[field]==source[field];checks+=1
  for file in state['frameFiles']:
   im=Image.open(HERE/file);assert im.mode=='RGBA' and im.size==(256,256);checks+=1
 for i in range(6):assert Image.open(HERE/start['frameFiles'][i]).tobytes()==Image.open(HERE/stop['frameFiles'][5-i]).tobytes();checks+=1
 for action,slot,loop,pivot in [('swim-start-east',0,'tread',[92,70]),('swim-start-east',5,'swim',[122,88]),('swim-stop-east',0,'swim',[122,88]),('swim-stop-east',5,'tread',[92,70])]:
  im=Image.new('RGBA',(256,256));path=ROOT/cov['selected']['bare'][loop+'-east']['files'][0] if variant=='bare' else HERE/f'frames/helmet/{loop}-east/000.png';im.alpha_composite(Image.open(path),(128-pivot[0],128-pivot[1]));assert im.tobytes()==Image.open(HERE/by[action]['frameFiles'][slot]).tobytes();checks+=1
(HERE/'east-transition-packaging-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'scope':'paired starts/stops, exact registered tread/swim joins, timing/medium/stride/canvas metadata','installed':False},indent=2)+'\n',encoding='utf-8');print(f'{checks} transition packaging/join checks pass.')
