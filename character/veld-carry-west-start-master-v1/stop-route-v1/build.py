from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;F=P.parent;R=P.parents[2];P.mkdir(exist_ok=True)
checks=0;bindings={}
for gear in ['bare','helmet']:
 data=json.loads((F/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 refs=['res://'+(R/f'character/veld-carry-west-master-proportions-v1/frames/{gear}/002.png').relative_to(R).as_posix()]+['res://'+(F/f'frames/{gear}/{i:03}.png').relative_to(R).as_posix() for i in [2,1,0]]
 state={'id':'carry-stop-phase2-west','frameFiles':refs,'frameDurationsMs':[80]*4,'frameCount':4,'loop':False,'facings':['west']*4,'waterKinds':['carry']*4,'waterPoses':[False]*4,'depthOffsets':[0.0]*4}
 data['states'].append(state);data.update(status='staged_phase2_stop_route_not_normal_controller')
 (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 frames=[]
 for ref in refs:
  source=R/ref.removeprefix('res://');bindings[ref]=hashlib.sha256(source.read_bytes()).hexdigest();bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(Image.open(source).convert('RGBA'));frames.append(bg)
 out=P/f'{gear}-stop-phase2-west.apng';frames[0].save(out,format='PNG',save_all=True,append_images=frames[1:],duration=[80]*4,loop=1,disposal=0,blend=0)
 with Image.open(out) as decoded:
  assert decoded.n_frames==4;checks+=1
  for i,frame in enumerate(frames):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==frame.tobytes();assert decoded.info['duration']==80;checks+=2
 assert refs[0].endswith('/002.png') and refs[-1].endswith('/000.png');checks+=1
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceBindings':bindings,'scope':'Whole existing authored aliases, exact carry2 stop entry and master held terminal;320ms source timing, route simulation remaps deceleration to actual remaining distance. No new generation, anatomy edits, normal adoption or general stop/safety acceptance.'},indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0}))
