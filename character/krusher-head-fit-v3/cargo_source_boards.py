from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-cargo-family-v3';O=P/'review/source';O.mkdir(parents=True,exist_ok=True)
rows=[q for q in json.loads((P/'revision.json').read_text())['records'] if q['changedPixels']];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),15)
for start in range(0,len(rows),48):
 chunk=rows[start:start+48];board=Image.new('RGB',(1440,35+((len(chunk)+7)//8)*180),'#252b2e');draw=ImageDraw.Draw(board);draw.text((10,5),'CARGO / REVISED COMPLETE HEAD AND COLLAR CONTEXTS',font=font,fill='white')
 for j,q in enumerate(chunk):
  ys,xs=np.where(np.array(Image.open(P/q['mask']))>0);cx=int((xs.min()+xs.max())//2);cy=int((ys.min()+ys.max())//2);crop=Image.open(P/q['output']).convert('RGBA').crop((cx-28,cy-24,cx+28,cy+28)).resize((168,156),Image.Resampling.NEAREST);x=j%8*180;y=25+j//8*180;board.paste(crop,(x,y),crop);draw.text((x,y+156),q['gear'][0]+' '+q['state']+' '+str(q['frame']),font=font,fill='white')
 board.save(O/f'heads-{start//48:02d}.png')
(O/'index.json').write_text(json.dumps({'changedDrawings':len(rows),'records':rows},indent=2)+'\n')
print(json.dumps({'changedDrawings':len(rows),'pages':(len(rows)+47)//48}))
