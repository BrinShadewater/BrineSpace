from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'cargo-boundary-audit-v1';D.mkdir(exist_ok=True)
canonical={'north':('north-west-candidate-v4','000'),'east':('north-east-candidate-v5','005'),'south':('candidate-v7','000')}
def resolve(p,key,slot):
 m=json.loads(p.read_text(encoding='utf-8'));s=next(s for s in m['states'] if s['id']==key);ref=s['frameFiles'][slot];return (R/ref[6:] if ref.startswith('res://') else p.parent/ref),s
records=[]
for direction in ['east','south','north','west']:
 for gear in ['bare','helmet']:
  items=[]
  if direction=='west':c=R/f'character/veld-cargo-west-master-family-v1/frames/{gear}/unload-west/000.png'
  else:folder,slot=canonical[direction];c=P/f'{folder}/frames/{gear}/{slot}.png'
  items.append(('Repaired held',c))
  for label,action,slot in [('Selected carry0','carry',0),('Selected carry3','carry',3),('Selected unload0','unload',0),('Selected pickup last','pickup',-1)]:
   manifest=R/f'character/veld-{action}-{direction}-consistent-v1/{gear}-manifest.json'
   if direction=='north' and gear=='helmet' and action=='carry':manifest=R/'character/veld-unified-turn-helmet-v1/carry-north-helmet-manifest.json'
   ref,state=resolve(manifest,action+'-'+direction,slot);items.append((label,ref))
  board=Image.new('RGB',(1280,488),'#202a30');draw=ImageDraw.Draw(board)
  for i,(label,path) in enumerate(items):
   im=Image.open(path).convert('RGBA');assert im.size==(256,256);a=np.array(im);y,x=np.where(a[:,:,3]>160);top=int(y.min());_,hx=np.where(a[top:top+20,:,3]>160)
   records.append({'direction':direction,'gear':gear,'label':label,'path':path.relative_to(R).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'headTop20Width':int(hx.max()-hx.min()+1),'alphaHeight':int(y.max()-y.min()+1),'equalsRepairedHeld':path.read_bytes()==c.read_bytes()})
   board.paste(im,(i*256,22),im);draw.text((i*256+4,4),direction+' '+gear+' '+label,fill='white')
   detail=im.crop((82,62,174,166)).resize((184,208),Image.Resampling.NEAREST);board.paste(detail,(i*256+36,280),detail)
  board.save(D/f'{gear}-{direction}-boundary.png')
(D/'audit.json').write_text(json.dumps({'presentations':len(records),'records':records,'visualReview':'pending','scope':'manifest-bound source comparison at same256canvas/p128224. North helmet carry honors later grid override. No actual controller/native/world admission.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps([(r['direction'],r['gear'],r['label'],r['headTop20Width']) for r in records if r['gear']=='bare']))
