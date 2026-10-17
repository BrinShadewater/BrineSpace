from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
r=Path(__file__).resolve().parents[2];out=r/'character/james-full-set-review-2026-10-02';f=out/'source-inventory.json';d=json.loads(f.read_bytes());files=[f,Path(__file__)];records=[]
for item in d['pairedContracts']:
 if item['sameCanvasPivotRuler']:continue
 state=item['state'];board=Image.new('RGBA',(768,564),(48,59,63,255));draw=ImageDraw.Draw(board)
 for row,kind in enumerate(('bare','helmet')):
  s=d['states'][kind][state];assert s['standingHeight']==148
  for col,slot in enumerate((0,s['frameCount']//2,s['frameCount']-1)):
   source=r/s['frameFiles'][slot];files.append(source);im=Image.open(source).convert('RGBA')
   assert im.size==(s['frameWidth'],s['frameHeight'])
   x=round(128-s['pivot'][0]);y=round(224-s['pivot'][1]);native=Image.new('RGBA',(256,256));native.alpha_composite(im,(x,y))
   board.alpha_composite(native,(col*256,row*282+26));draw.text((col*256+4,row*282+7),kind+' '+state+' '+str(slot),fill='white')
   records.append({'state':state,'kind':kind,'slot':slot,'source':source.relative_to(r).as_posix(),'translation':[x,y],'nativeAlpha128Bounds':native.getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox()})
 board.convert('RGB').save(out/(state+'-profile-pair.png'))
report={'records':records,'inputSha256':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},'visualReviewPending':True,'normalChanged':False,'scope':'Eight existing meal/drink bare/helmet profile differences: same148 ruler and physical pivot translation, three prescribed source slots each. Static source comparison only; real meal scheduler/equipment use/furniture/continuous motion unverified.'}
(out/'profile-pair-review.json').write_text(json.dumps(report,indent=2)+'\n');print('Eight paired meal/drink profile boards;48 exact source references.')
