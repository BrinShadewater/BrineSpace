from pathlib import Path
from PIL import Image,ImageDraw
import json,sys
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/(sys.argv[1] if len(sys.argv)>1 else 'arrival-journey-v323')
d=json.loads((o/'native-evidence.json').read_bytes());rows=[]
for result in d['results']:
 mode='bare' if result['gear']=='' else 'helmet';files=[r/f[6:] for f in result['captures']]
 for start in range(0,len(files),8):
  batch=files[start:start+8];board=Image.new('RGB',(800,380),(47,58,62));draw=ImageDraw.Draw(board)
  for i,f in enumerate(batch):
   im=Image.open(f).convert('RGB');cx=im.width//2;cy=im.width//2
   # The original world capture is square around the foot. Bottom viewport
   # clipping can shorten its height; it does not move the foot to the new centre.
   # Exact screenshot region around actor; no scaling or artwork adjustment.
   crop=im.crop((cx-80,cy-110,cx+80,cy+30));x=(i%4)*200;y=(i//4)*190
   board.paste(crop,(x+20,y+35));draw.text((x+4,y+4),f.stem.replace(mode+'-',''),fill='white')
  name=f'{mode}-native-review-{start:02d}.png';board.save(o/name);rows.append(name)
(o/'review-boards.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(captures=sum(len(x['captures']) for x in d['results']),boards=rows)))
