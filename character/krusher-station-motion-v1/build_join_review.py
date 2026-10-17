from pathlib import Path
import json,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent
lib=json.loads((R/'character/krusher-continuous-playback-v1/library.json').read_text());states=lib['states']
plans=[p for p in lib['plans'] if len(p['segments'])>1]
scale=65.28/148
out=H/'joins';out.mkdir(exist_ok=True)
for page in range(math.ceil(len(plans)/12)):
 board=Image.new('RGB',(1200,12*160+40),'#1b272d');d=ImageDraw.Draw(board)
 d.text((8,8),'Krusher V11 | 65.28px world standing ruler | entry end > target first/mid/last > destination first | nearest pixels',fill='white')
 for row,p in enumerate(plans[page*12:page*12+12]):
  y=40+row*160;d.text((8,y),p['key'],fill='#d3dfe4')
  segments=p['segments'];first=states[segments[0]['key']];target=states[p['key']];last=states[segments[-1]['key']]
  picks=[(first,-2),(first,-1),(target,0),(target,len(target['files'])//2),(target,-1),(last,0),(last,1)]
  for col,(s,i) in enumerate(picks):
   i=max(0,min(i if i>=0 else len(s['files'])+i,len(s['files'])-1));im=Image.open(R/s['files'][i].lstrip('/')).convert('RGBA')
   im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
   x=10+col*170;px=x+78-round(s['pivot'][0]*scale);py=y+96-round(s['pivot'][1]*scale)
   board.paste(im,(px,py),im);d.line((x+72,y+96,x+84,y+96),fill='#52656b')
 board.save(out/('joins-%02d.png'%page))
(H/'join-review.json').write_text(json.dumps({'plans':len(plans),'turns':sum('-turn-' in p['key'] for p in plans),'worldStandingRuler':65.28,'scale':scale,'pages':math.ceil(len(plans)/12),'scope':'Pivot-aligned source handoff witnesses at world actor scale; not actual furniture depth or natural controller coverage.'},indent=2))
print('Prepared',len(plans),'transition rows in',math.ceil(len(plans)/12),'sheets')
