from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),18)
for folder,originalVersion,newVersion in [('water-family',1,4),('water-cargo-turns',2,4),('water-interruptions',1,3)]:
 P=R/f'character/krusher-{folder}-v{newVersion}';OLD=R/f'character/krusher-{folder}-v{originalVersion}';rows=json.loads((P/'revision.json').read_text())['records'];orig={q['output']:q for q in json.loads((OLD/'provenance.json').read_text())['records']};samples=[]
 for g in ['bare','helmet']:
  if folder=='water-cargo-turns':
   for v in ['south','se','east','ne','north','nw','west','sw']:
    seq=[q for q in rows if q['gear']==g and q['details'].get('view')==v];samples.append(seq[len(seq)//2])
  else:
   for d in ['east','south','west','north']:
    prefixes=['swim-start','swim'] if folder=='water-family' else ['swim-cancel-pickup-0','swim-distress']
    for prefix in prefixes:
     seq=[q for q in rows if q['gear']==g and q['state']==prefix+'-'+d];samples.append(seq[len(seq)//2])
 board=Image.new('RGBA',(1000,880),'#252b2e');draw=ImageDraw.Draw(board)
 for i,q in enumerate(samples):
  a=Image.open(P/q['output']).convert('RGBA');d=q['details'];oq=orig[q['output']];x0,y0,x1,y1=oq['headBox'];cx=round((x0+x1)/2);cy=round((y0+y1)/2);crop=a.crop((cx-32,cy-32,cx+32,cy+32)).resize((192,192),Image.Resampling.NEAREST);x=i%4*250+20;y=i//4*220;board.alpha_composite(crop,(x,y));draw.text((x,y+195),q['gear']+' '+str(d.get('view'))+' '+str(q['frame']),font=font,fill='white')
 board.save(H/(folder+'-head-review.png'));print(folder,len(samples))
