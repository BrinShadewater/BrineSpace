from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];reg=json.loads((P/'head-registration.json').read_text());b=Image.new('RGB',(2048,768),(34,52,62));dr=ImageDraw.Draw(b)
choices=[r for r in reg['frames'] if r['gear']=='bare' and ((r['state']=='pickup-north' and r['frame'] in [1,2,4,5,7]) or (r['state']=='carry-north' and r['frame'] in [0,3]) or (r['state']=='unload-north' and r['frame']==2))]
for col,r in enumerate(choices):
 box=(int(r['headAxis'])-30,r['sourceTop']-8,int(r['headAxis'])+40,r['sourceTop']+55)
 for row,f in enumerate([r['bareFile'],r['output'],r['output'].replace('/bare/','/helmet/')]):
  im=Image.open(R/f[6:]).convert('RGBA').crop(box).resize((210,189),Image.Resampling.NEAREST);b.paste(im,(col*256,row*256),im);dr.text((col*256+4,row*256+210),r['state']+' '+str(r['frame']),fill='white')
b.save(P/'neck-review.png')
