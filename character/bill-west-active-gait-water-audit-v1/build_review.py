from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
review=json.loads((OUT/'review.json').read_text())
for n,h in review['inputSHA256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
master=Image.open(ROOT/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png').convert('RGBA')
master=master.resize((round(master.width*148/956),round(master.height*148/956)),Image.Resampling.LANCZOS)
mc=Image.new('RGBA',(352,320));mc.alpha_composite(master,(160-master.width//2,224-master.height))
for gear in ['bare','helmet']:
 items=[('Original West / bare authority',mc)]
 for tick in [67,445]:
  i=review['actualNativeTickMatches'][gear+str(tick)]
  im=Image.open(ROOT/f'character/bill-walk-west-material-v1/frames/{gear}/walk-west/{i:03}.png').convert('RGBA')
  canvas=Image.new('RGBA',(352,320));canvas.alpha_composite(im,(32,0));items.append((f'Actual walk tick{tick} / frame{i}',canvas))
 for bank,state,i,label in [('bill-land-water-west-v15','land-swim-west',1,'Ready'),('bill-land-water-west-v15','land-swim-west',2,'Crouch'),('bill-water-exit-west-master-v13','swim-land-west',6,'Rise'),('bill-swim-west-calibrated-v6','swim-west',0,'Extend')]:
  items.append((label,Image.open(ROOT/f'character/{bank}/{gear}/frames/{state}/{i:03}.png').convert('RGBA')))
 board=Image.new('RGB',(2464,720),(23,42,51));draw=ImageDraw.Draw(board)
 for col,(name,im) in enumerate(items):
  draw.text((352*col+5,5),gear+' / '+name,fill='white');board.paste(im,(352*col,28),im)
  if col<6:
   crop=im.crop((120,55,190,145)).resize((210,270),Image.Resampling.NEAREST);board.paste(crop,(352*col+70,385),crop)
 board.save(OUT/(gear+'-master-join-review.png'))
print('Frozen source hashes pass; two master/join boards rebuilt without artwork alteration.')
