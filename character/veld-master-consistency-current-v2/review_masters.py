"""Current selected sources beside unchanged original cardinal masters."""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
R=P.parents[1]
raw=(P/'selected-library.json').read_bytes(); inventory=json.loads(raw)
masters={
 'east':('character/veld-side-foundation-v1/east-standing.png',[92,172]),
 'west':('character/veld-side-foundation-v1/west-standing.png',[92,172]),
 'north':('character/veld-idle-north-original-master-v1/original-idle-master.png',[128,224]),
 'south':('character/veld-idle-south-original-master-v1/original-idle-master.png',[128,224])}
rows=[]; bindings={}; boards=[]
actions=['idle','walk','interact','carry','pickup','unload','repair']
for direction,(master,pivot) in masters.items():
 board=Image.new('RGB',(2048,1200),'#202a30');draw=ImageDraw.Draw(board)
 for gi,gear in enumerate(['bare','helmet']):
  for phase in range(2):
   y=(gi*2+phase)*300
   im=Image.open(R/master).convert('RGBA')
   board.paste(im,(128-pivot[0],y+30+224-pivot[1]),im)
   draw.text((5,y+5),'ORIGINAL BARE '+direction,fill='white')
   bindings[master]=hashlib.sha256((R/master).read_bytes()).hexdigest()
   for col,action in enumerate(actions,1):
    state=action+'-'+direction; entry=inventory['resolved'][gear].get(state)
    if entry is None:
     draw.text((col*256+5,y+5),'Absent '+state,fill='white');continue
    assert entry['standingHeight']==148,(state,entry['standingHeight'])
    index=0 if phase==0 else len(entry['frameFiles'])//2
    source=entry['frameFiles'][index];path=R/source
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest==inventory['sourceBindings'][source],source
    bindings[source]=digest;im=Image.open(path).convert('RGBA');px,py=entry['pivot']
    board.paste(im,(col*256+128-round(px),y+30+224-round(py)),im)
    draw.text((col*256+5,y+5),f'{gear} {state} / {index}',fill='white')
    rows.append(dict(gear=gear,state=state,index=index,source=source,manifest=entry['manifest'],pivot=entry['pivot'],paddingOnly=[128-round(px),224-round(py)]))
 name=direction+'-selected-master-review.png';board.save(P/name);boards.append(name)
(P/'master-review-evidence.json').write_text(json.dumps(dict(boards=boards,rows=rows,bindings=bindings,inventorySHA256=hashlib.sha256(raw).hexdigest(),visualReview='pending',scope='First/middle selected dry sources at unchanged native scale and original colour, fixed pivot padding only. Bare masters in all rows are body/identity references, not helmet references. Static samples do not prove full motion/contact/native integration.'),indent=2)+'\n')
print(f'{len(boards)} boards; {len(rows)} selected presentations; {len(bindings)} unchanged bound images')
