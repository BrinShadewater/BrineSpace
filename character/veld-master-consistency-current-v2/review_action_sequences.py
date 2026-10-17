from review_masters import P,R,inventory,masters
from PIL import Image,ImageDraw
import json,hashlib
records=[];boards=[]
for direction in ['west','north','south']:
 actions=['interact','repair'];columns=max(len(inventory['resolved']['bare'][a+'-'+direction]['frameFiles']) for a in actions)+1
 board=Image.new('RGB',(columns*256,600),'#202a30');draw=ImageDraw.Draw(board)
 for ri,action in enumerate(actions):
  master,pivot=masters[direction];im=Image.open(R/master).convert('RGBA');y=ri*300
  board.paste(im,(128-pivot[0],y+30+224-pivot[1]),im);draw.text((5,y+5),'ORIGINAL '+direction,fill='white')
  state=action+'-'+direction;entry=inventory['resolved']['bare'][state]
  for i,source in enumerate(entry['frameFiles']):
   digest=hashlib.sha256((R/source).read_bytes()).hexdigest();assert digest==inventory['sourceBindings'][source]
   im=Image.open(R/source).convert('RGBA');px,py=entry['pivot'];x=(i+1)*256
   board.paste(im,(x+128-round(px),y+30+224-round(py)),im);draw.text((x+5,y+5),f'{state} / {i}',fill='white')
   records.append(dict(state=state,index=i,source=source,SHA256=digest,manifest=entry['manifest']))
 name=direction+'-full-action-review.png';board.save(P/name);boards.append(name)
(P/'action-sequence-evidence.json').write_text(json.dumps(dict(boards=boards,rows=records,visualReview='pending',scope='Every selected bare interact/repair source in West/North/South; original colour/native scale/pivot padding only. Source pose review, not continuous native motion.'),indent=2)+'\n')
print(f'{len(records)} complete action-source presentations')
