from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np,sys
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for family in sys.argv[1:] or ['repair','torch','seated']:
 P=R/f'character/krusher-{family}-family-v4';records=json.loads((P/'revision.json').read_text())['records'];sample=[]
 for gear in ['bare','helmet']:
  for d in ['south','east','north','west']:
   rows=[q for q in records if q['gear']==gear and q['state'].endswith(d) and 'headSource' in q['details']]
   if rows:sample.extend([rows[0],rows[len(rows)//2],rows[-1]])
 b=Image.new('RGBA',(1200,60+((len(sample)+7)//8)*220),'#252b2e');draw=ImageDraw.Draw(b);draw.text((12,10),family.upper()+' / HEAD AND COLLAR FIT / ENTRY, WORK, EXIT',font=font,fill='white')
 for i,q in enumerate(sample):
  im=Image.open(P/q['output']).convert('RGBA');mask=np.array(Image.open(P/q['mask']).convert('L'))>0;y,x=np.where(mask);cx=(int(x.min())+int(x.max()))//2;cy=(int(y.min())+int(y.max()))//2;crop=im.crop((cx-24,cy-22,cx+24,cy+35)).resize((144,171),Image.Resampling.NEAREST);px=i%8*150;py=i//8*220+45;b.alpha_composite(crop,(px,py));draw.text((px+2,py+173),q['gear'][0]+' '+q['state'],font=font,fill='white');draw.text((px+2,py+194),str(q['frame']),font=font,fill='#bfd2d4')
 b.save(H/(family+'-fit-review.png'));print(family,len(sample))
