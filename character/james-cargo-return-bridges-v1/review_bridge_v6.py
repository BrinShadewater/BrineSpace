from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
board=Image.new('RGB',(1792,620),'#303b40');draw=ImageDraw.Draw(board)
refs=json.loads((p/'reference-evidence.json').read_bytes())
assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in refs['sources'])
reference=Image.open(p/'west-bridge-reference.png').convert('RGBA')
for row,mode in enumerate(['bare','helmet']):
 manifest=json.loads((p/(mode+'-joined-manifest-v6.json')).read_bytes())
 files=manifest['states'][0]['frameFiles']
 for col,ref in enumerate(files):
  path=r/ref.removeprefix('res://') if ref.startswith('res://') else p/ref
  source=Image.open(path).convert('RGBA')
  x=col*256;y=row*310
  draw.text((x+5,y+5),mode+' / '+('original carry' if col==0 else 'original unload' if col==5 else 'v6 '+str(col)),fill='white')
  board.paste(source,(x,y+28),source)
  draw.line((x,y+252,x+255,y+252),fill='#a6b0b0')
 master=reference.crop((512,row*256,768,(row+1)*256))
 board.paste(master,(1536,row*310+28),master)
 draw.text((1541,row*310+5),mode+' / original idle',fill='white')
 draw.line((1536,row*310+252,1791,row*310+252),fill='#a6b0b0')
board.save(p/'bridge-v6-registered-review.png')
print('14registered source presentations; six reference hashes unchanged; full-body candidate unselected.')
