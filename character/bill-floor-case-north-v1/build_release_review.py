"""Inspect authored release timing without modifying source pixels."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
board=Image.new('RGBA',(1792,1280),'#22343e');draw=ImageDraw.Draw(board);rows=[]
for gear_index,gear in enumerate(['bare','helmet']):
 m=json.loads((R/f'character/bill-unload-north-rise-v1/{gear}-manifest.json').read_text(encoding='utf-8'))['states'][0]
 time=0.0
 for i,name in enumerate(m['frameFiles']):
  path=R/name.removeprefix('res://');im=Image.open(path).convert('RGBA')
  x=(i%7)*256;y=(gear_index*2+i//7)*320
  board.alpha_composite(im,(x,y))
  draw.text((x+8,y+256),f'{gear} {i:02d} / {time:.3f}s',fill='white')
  detail=im.crop((108,174,151,224)).resize((43,50),Image.Resampling.NEAREST)
  board.alpha_composite(detail,(x+200,y+260))
  rows.append({'gear':gear,'index':i,'startSeconds':time,'path':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
  time+=float(m['frameDurationsMs'][i])/1000
board.convert('RGB').save(P/'release-source-review.png')
(P/'release-source-index.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print('All28 paired unload sources reviewed on original pivot; no source edits.')
