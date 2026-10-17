from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent;r=p.parents[1]
version='v4' if '--v4' in sys.argv else 'v3' if '--v3' in sys.argv else ''
frame_dir='frames-'+version if version else 'frames'
suffix='-'+version if version else ''
refs=json.loads((p/'reference-evidence.json').read_bytes())['sources']
board=Image.new('RGB',(1536,576),'#303b40');draw=ImageDraw.Draw(board)
for row,mode in enumerate(('bare','helmet')):
 sources=[(x['path'],x['pivot'],x['key']) for x in refs if x['mode']==mode]
 chosen=[sources[0]]+[(str((p/f'{frame_dir}/{mode}/{i:03d}.png').relative_to(r)),[128,224],f'new bridge {i}') for i in range(3)]+sources[1:]
 for col,(rel,pivot,label) in enumerate(chosen):
  im=Image.open(r/rel).convert('RGBA');x=col*256;y=row*288
  draw.text((x+4,y+4),f'{mode}: {label}',fill='white')
  board.paste(im,(x+128-int(pivot[0]),y+30+224-int(pivot[1])),im)
  draw.line((x,y+254,x+255,y+254),fill='#929d9f')
board.save(p/f'west-bridge-endpoint-review{suffix}.png')
station=board.resize((492,184),Image.Resampling.NEAREST);station.save(p/f'west-bridge-station-review{suffix}.png')
hashes={str(x.relative_to(r)):hashlib.sha256(x.read_bytes()).hexdigest() for x in p.glob(f'{frame_dir}/*/*.png')}
(p/f'study-source-hashes{suffix}.json').write_text(json.dumps(hashes,indent=2)+'\n')
print('All six bridge sources presented beside exact endpoints and idle at full and reduced scales.')
