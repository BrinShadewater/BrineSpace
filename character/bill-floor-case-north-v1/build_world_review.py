"""Retain all original native captures; compare at a fixed floor anchor."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-world-v1'
d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert v['passed'] and d['failures']==0 and len(d['records'])==12
C=P/'world-captures';C.mkdir(exist_ok=True)
for gear in ['bare','helmet']:
 rows=[r for r in d['records'] if r['name'].startswith(gear+'-')]
 assert len(rows)==6
 root=rows[0]['foot'];x=255+(root[0]-7680)*398/384;y=287+(root[1]-8064)*398/384
 board=Image.new('RGB',(len(rows)*200,240),'#182932');draw=ImageDraw.Draw(board)
 for i,r in enumerate(rows):
  for kind in ['room','source']:
   name=r['name']+'-'+kind+'.png';shutil.copy2(O/name,C/name)
  im=Image.open(O/(r['name']+'-room.png')).convert('RGB')
  board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(i*200+10,35))
  draw.text((i*200+10,8),r['name'],fill='#dde8e9')
  draw.text((i*200+10,220),'case fixed' if r['caseEnabled'] else 'baseline',fill='#dde8e9')
 board.save(P/(gear+'-world-review.png'))
page='''<!doctype html><meta charset="utf-8"><title>Bill floor case · native study</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}figure{margin:25px 0;overflow:auto}img{max-width:none}p{max-width:850px}a{color:#adcddd}</style><h1>Bill · fixed floor case native study</h1><p>Actual selected Bill carry/unload and next-activity departure, with an explicitly staged workshop prop renderer. Crops retain one fixed floor anchor as Bill moves. Original screenshots are copied unchanged; these boards crop them for review.</p><p>Case is selected only in this fixture. World ownership, lifetime, Continue and normal integration remain pending. Static samples do not certify full continuous motion/contact.</p><figure><img src="bare-world-review.png"></figure><figure><img src="helmet-world-review.png"></figure><p><a href="./">Registered source study</a></p>'''
(P/'world-review.html').write_text(page,encoding='utf-8')
print('12 native room/source pairs retained; fixed-anchor boards prepared.')
