from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'half-turn-candidate-v1';D.mkdir(exist_ok=True)
packages={'north-east':'north-east-candidate-v5','east-south':'east-south-candidate-v3','south-west':'candidate-v7','north-west':'north-west-candidate-v4'}
routes={'east-west':[('east-south',False),('south-west',False)],'west-east':[('north-west',True),('north-east',False)],'north-south':[('north-east',False),('east-south',False)],'south-north':[('south-west',False),('north-west',True)]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
provenance={};checks=0
for gear in ['bare','helmet']:
 old=R/f'character/veld-carry-half-turns-consistent-v1/{gear}-manifest.json';manifest=json.loads(old.read_text(encoding='utf-8'))
 for state in manifest['states']:
  action=state['id'].removeprefix('carry-turn-');refs=[]
  for pair,reverse in routes[action]:
   row=[P/packages[pair]/f'frames/{gear}/{i:03}.png' for i in range(6)]
   refs+=list(reversed(row)) if reverse else row
  assert len(refs)==len(state['frameFiles'])==12;checks+=1
  assert refs[5].read_bytes()==refs[6].read_bytes();checks+=1
  board=Image.new('RGB',(1536,600),'#202a30');draw=ImageDraw.Draw(board);paths=[]
  for i,ref in enumerate(refs):
   dst=D/f'frames/{gear}/{action}/{i:03}.png';dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(ref.read_bytes());assert dst.read_bytes()==ref.read_bytes();checks+=1
   paths.append('res://'+dst.relative_to(R).as_posix());provenance[dst.relative_to(D).as_posix()]={'quarterSource':ref.relative_to(R).as_posix(),'sha256':sha(ref)}
   im=Image.open(dst).convert('RGBA');x=i%6*256;y=i//6*300;board.paste(im,(x,y+22),im);draw.text((x+4,y+4),gear+' '+action+' '+str(i),fill='white')
  state['frameFiles']=paths;assert sum(state['frameDurationsMs'])==680 and not state['loop'];checks+=1
  board.save(D/f'{gear}-{action}-contact.png')
 manifest.update(name='Veld master cargo half turns '+gear,status='staged_not_installed');(D/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(D/'registration.json').write_text(json.dumps({'routes':routes,'quarterPackages':packages,'frameBindings':provenance,'checks':checks,'failures':0,'duplicateMidpointWholeFramesExact':True,'status':'staged_not_installed','scope':'deterministic concatenation of reviewed authored whole quarter poses; original680ms metadata; no new anatomy, normal selection or world/lifecycle acceptance'},indent=2)+'\n',encoding='utf-8')
print(str(checks)+' route/export/finite checks;96source-bound exports/eight states/four paired routes, original680ms')
