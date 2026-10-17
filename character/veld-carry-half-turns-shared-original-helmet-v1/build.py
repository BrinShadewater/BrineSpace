from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];Q=R/'character/veld-helmet-original-turntable-west-v1';B=R/'character/veld-cargo-turns-master-family-v1/half-turn-candidate-v1'
routes={'east-west':['east-south','south-west'],'west-east':['west-north','north-east'],'north-south':['north-east','east-south'],'south-north':['south-west','west-north']}
checks=0;bindings={};endpoints={}
for gear in ['bare','helmet']:
 m=json.loads((B/f'{gear}-manifest.json').read_text());q=json.loads((Q/f'{gear}-manifest.json').read_text());states={s['id'].removeprefix('carry-turn-'):s for s in q['states']}
 for s in m['states']:
  route=s['id'].removeprefix('carry-turn-');pairs=routes[route];refs=states[pairs[0]]['frameFiles']+states[pairs[1]]['frameFiles'];assert len(refs)==12;checks+=1
  assert (R/refs[5][6:]).read_bytes()==(R/refs[6][6:]).read_bytes();checks+=1
  board=Image.new('RGB',(1536,600),'#202a30');d=ImageDraw.Draw(board)
  for i,ref in enumerate(refs):
   f=R/ref[6:];bindings[ref]=hashlib.sha256(f.read_bytes()).hexdigest()
   if gear=='bare':assert f.read_bytes()==(R/s['frameFiles'][i][6:]).read_bytes();checks+=1
   im=Image.open(f).convert('RGBA');x=i%6*256;y=i//6*300;board.paste(im,(x,y+22),im);d.text((x+4,y+4),gear+' '+route+' '+str(i),fill='white')
  s['frameFiles']=refs;assert not s['loop'] and sum(s['frameDurationsMs'])==680;checks+=1
  endpoints[gear+'-'+route]={'quarters':pairs,'first':refs[0],'last':refs[-1],'midpoint':[refs[5],refs[6]]};board.save(P/f'{gear}-{route}-contact.png')
 m['name']='Veld shared original helmet half turns '+gear;m['status']='staged_not_installed';(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'routes':routes,'endpoints':endpoints,'bindings':bindings,'durationMs':680,'scope':'Exact source reuse from shared quarters; original finite metadata and bare bodies unchanged. No new raster art or normal/controller/world/idle-cargo joins acceptance.'},indent=2)+'\n')
print(str(checks)+' source/bare-body/midpoint/timing checks0')
