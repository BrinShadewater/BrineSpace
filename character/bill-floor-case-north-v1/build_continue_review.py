"""Unmodified native Continue pairs, crop focus tied to the saved physical root."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-continue-v1'
d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
assert v['passed'] and d['failures']==0 and len(d['records'])==8
C=P/'continue-captures';C.mkdir(exist_ok=True)
for gear in ['bare','helmet']:
 board=Image.new('RGB',(800,250),'#182932');draw=ImageDraw.Draw(board)
 for pair,phase in enumerate(['terminal','deposited']):
  rows=[r for r in d['records'] if r['name'].startswith(gear+'-'+phase+'-')];assert len(rows)==2
  root=rows[0]['foot'];x=255+(root[0]-7680)*398/384;y=287+(root[1]-8064)*398/384
  for j,r in enumerate(rows):
   i=pair*2+j
   for kind in ['room','source']:
    name=r['name']+'-'+kind+'.png';shutil.copy2(O/name,C/name)
   im=Image.open(O/(r['name']+'-room.png')).convert('RGB');board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(i*200+10,40))
   draw.text((i*200+10,8),r['name'],fill='#dde8e9')
   draw.text((i*200+10,225),'case retained' if r['caseEnabled'] else 'deposit pending',fill='#dde8e9')
 board.save(P/(gear+'-continue-review.png'))
page='''<!doctype html><meta charset="utf-8"><title>Bill floor case Continue</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:850px}figure{margin:25px 0;overflow:auto}img{max-width:none}a{color:#adcddd}</style><h1>Bill · staged floor-case Continue</h1><p>Four ordinary disk/fresh-main restores, guarded by staged floor-state validation and observer. Both gears: terminal before deposit and departed with case deposited. Native before/after screenshots copied unchanged; thirty future actor/source/case ticks match.</p><p>Normal actor/player preserved. Floor state and renderer remain fixture-selected; no normal title/loader admission or full continuous-motion acceptance.</p><figure><img src="bare-continue-review.png"></figure><figure><img src="helmet-continue-review.png"></figure><a href="world-review.html">Native departure review</a> · <a href="./">Source study</a>'''
(P/'continue-review.html').write_text(page,encoding='utf-8');print('Four native Continue comparison pairs retained.')
