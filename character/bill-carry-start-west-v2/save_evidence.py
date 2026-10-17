from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parent.parent;G=R/'character/bill-carry-west-gait-v2'
jobs=[(G,'first-v1.png','prompt-first-v1.txt','exec-12312ec7-574c-4850-9ce3-219a5d40d869','accepted first support half; standing calibration3'),(G,'opposite-v2.png','prompt-opposite-v2.txt','exec-370887e6-72e5-4984-bf24-98ed73f40865','accepted opposite support half; standing calibration3'),(P,'first-step-rejected-v1.png','prompt-first-step-v1.txt','exec-e45bb8f5-add5-42b6-bd28-5cf3b500304d','rejected: first three poses already near full stride, insufficient gradual entrance; never packaged or run'),(P,'first-step-v2.png','prompt-first-step-v2.txt','exec-fab46c1f-e0bb-4e44-b9ee-23e8be1be346','accepted small standing weight shifts0..2; standing calibration3')]
for root,raw,prompt,job,use in jobs:
 data={'provider':'built-in imagegen','execution':job,'rawSource':raw,'sha256':hashlib.sha256((root/'sources'/raw).read_bytes()).hexdigest(),'promptFile':prompt,'use':use,'referenceRoles':{'originalWestHeldMaster':'Identity, physique, full standing ruler','masterLegDetail':'Dim beveled rectangular plates, grain, straps and boot hardware'},'fit':json.loads((root/'registration.json').read_text()) if 'rejected' not in raw else None}
 (root/'sources'/f'{Path(raw).stem}-generation-evidence.json').write_text(json.dumps(data,indent=2)+'\n')
frames=[]
for ms in range(-240,1960,20):
 b=Image.new('RGB',(512,560),'#22343e');d=ImageDraw.Draw(b)
 for row,gear in enumerate(['bare','helmet']):
  master=R/f'character/bill-cargo-west-master-head-v1/frames/{gear}/pickup-west/011.png'
  if ms<0:path=master
  elif ms<320:
   clock=0
   for i,dt in enumerate([40,50,55,65,65,45]):
    clock+=dt
    if ms<clock:break
   path=P/f'frames/{gear}/carry-start-west/{i:03}.png'
  else:path=G/f'frames/{gear}/carry-west/{int(((ms-320+139)%840)//140):03}.png'
  for col,path in enumerate([master,path]):
   a=Image.open(path).convert('RGBA');b.paste(a,(col*256,row*280),a)
  d.text((8,row*280+260),gear+' master / first step and walk',fill='white')
 frames.append(b)
sheet=Image.new('RGB',(512,560*len(frames)))
for i,b in enumerate(frames):sheet.paste(b,(0,i*560))
pal=sheet.quantize(colors=255);frames=[b.quantize(palette=pal,dither=Image.Dither.NONE) for b in frames];frames[0].save(P/'master-first-step.gif',save_all=True,append_images=frames[1:],duration=20,loop=0)
print('Saved generation provenance and fixed-pivot source-clock replay')
