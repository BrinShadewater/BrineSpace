from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;C=R/'character/krusher-james-canonical-v7'
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),26);small=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),23);b=Image.new('RGBA',(720,1910),'#252b2e');draw=ImageDraw.Draw(b)
draw.text((24,15),'KRUSHER DOM / HEAD FIT REVIEW',font=font,fill='white');draw.text((90,52),'BARE',font=small,fill='#bfd2d4');draw.text((450,52),'HELMET',font=small,fill='#bfd2d4')
records=[]
for row,name in enumerate(['south','east','west','north','repair-east','seated-east']):
 for col,g in enumerate(['bare','helmet']):
  if '-' not in name:
   m=json.loads((C/(g+'-manifest.json')).read_text());s=next(s for s in m['states'] if s['id']=='idle-'+name);src=C/s['frameFiles'][0];cx,cy=92,39
  else:
   family='repair' if name.startswith('repair') else 'seated';P=R/f'character/krusher-{family}-family-v4';qs=json.loads((P/'revision.json').read_text())['records'];rows=[q for q in qs if q['gear']==g and q['state']==('repair-east' if family=='repair' else 'read-seated-enter-east') and 'headSource' in q['details']];q=rows[len(rows)//2];src=P/q['output'];head=Image.open(R/q['details']['headSource'][6:]);cx=q['details']['paste'][0]+head.width//2;cy=q['details']['paste'][1]+head.height//2+2
  im=Image.open(src).convert('RGBA');box=(cx-28,cy-24,cx+28,cy+36);crop=im.crop(box).resize((224,240),Image.Resampling.NEAREST);x=col*360+65;y=90+row*300;b.alpha_composite(crop,(x,y));draw.text((col*360+65,y+242),name.upper().replace('-',' / '),font=small,fill='white');records.append({'view':name,'gear':g,'source':src.relative_to(R).as_posix(),'crop':box,'displayScale':4})
b.save(H/'mobile-head-review.png');(H/'mobile-head-review.json').write_text(json.dumps({'method':'Current native candidate frames, crop-only4x nearest. Two-column portrait layout for mobile.','records':records},indent=2)+'\n');print('Mobile head review rendered from12current frames.')
