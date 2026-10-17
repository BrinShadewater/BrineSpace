from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for family in ['recovery-salvage','death-family']:
 P=R/f'character/krusher-{family}-v3';rows=json.loads((P/'revision.json').read_text())['records'];samples=[];isdeath=family=='death-family'
 for g in ['bare','helmet']:
  groups=['death-ground','death-water'] if isdeath else ['recover-air','salvage']
  for prefix in groups:
   for d in ['east','south','west','north']:
    seq=[q for q in rows if q['gear']==g and q['state']==prefix+'-'+d];samples.append(seq[-1] if isdeath else seq[len(seq)//2])
 board=Image.new('RGBA',(1000,880),'#252b2e');draw=ImageDraw.Draw(board)
 for i,q in enumerate(samples):
  a=Image.open(P/q['output']).convert('RGBA');d=q['details'];at=d.get('paste',[110,80]);cx=at[0]+(Image.open(R/d['headSource'][6:]).width//2 if 'headSource' in d else 15);cy=at[1]+(Image.open(R/d['headSource'][6:]).height//2 if 'headSource' in d else 15);crop=a.crop((cx-32,cy-30,cx+32,cy+34)).resize((192,192),Image.Resampling.NEAREST);x=i%4*250+20;y=i//4*220;board.alpha_composite(crop,(x,y));draw.text((x,y+195),q['gear']+' '+q['state'],font=font,fill='white')
 name='death' if isdeath else family;board.save(H/(name+'-head-review.png'))
 if isdeath:
  board=Image.new('RGBA',(1000,1480),'#252b2e');draw=ImageDraw.Draw(board)
  for i,q in enumerate(samples):
   a=Image.open(P/q['output']).convert('RGBA');crop=a.crop((10,10,246,350));x=i%4*250;y=i//4*370;board.alpha_composite(crop,(x,y));draw.text((x+3,y+345),q['gear']+' '+q['state'],font=font,fill='white')
  board.save(H/'death-body-review.png')
 print(name,len(samples))
