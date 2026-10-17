from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-james-canonical-v8'
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24);board=Image.new('RGBA',(900,760),'#252b2e');draw=ImageDraw.Draw(board);draw.text((24,15),'KRUSHER DOM / NATIVE STANDING PREVIEW',font=font,fill='white');close=Image.new('RGBA',(1000,420),'#252b2e');cd=ImageDraw.Draw(close);records=[]
for row,g in enumerate(['bare','helmet']):
 m=json.loads((P/(g+'-manifest.json')).read_text())
 for col,d in enumerate(['south','east','north','west']):
  s=next(s for s in m['states'] if s['id']=='idle-'+d);src=P/s['frameFiles'][0];im=Image.open(src).convert('RGBA');target=H/'standing'/f'{g}-{d}.png';im.save(target)
  crop=im.crop((55,12,129,180)).resize((148,336),Image.Resampling.NEAREST);x=col*220+35;y=row*350+65;board.alpha_composite(crop,(x,y));draw.text((x,y-28),d+' / '+g,font=font,fill='#bfd2d4')
  crop=im.crop((70,16,112,58)).resize((168,168),Image.Resampling.NEAREST);x=col*250+35;y=row*205+30;close.alpha_composite(crop,(x,y));cd.text((x,y-26),d+' / '+g,font=font,fill='white')
  records.append({'gear':g,'direction':d,'source':src.relative_to(R).as_posix(),'sourceHash':hashlib.sha256(src.read_bytes()).hexdigest(),'output':target.relative_to(H).as_posix(),'outputHash':hashlib.sha256(target.read_bytes()).hexdigest(),'displayScale':2})
board.save(H/'standing-review-mobile.png');close.save(H/'standing-heads-closeup.png');(H/'standing-verification.json').write_text(json.dumps({'status':'V5 canonical native candidate; remaining action/life/water families unchanged','method':'Exact first native idle frames from v8 standing manifests. No art edits in this rendering step.','records':records},indent=2)+'\n');print('Eight current canonical views rendered.')
