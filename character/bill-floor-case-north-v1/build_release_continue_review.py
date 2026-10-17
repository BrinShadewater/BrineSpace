from pathlib import Path
import json,shutil,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-release-continue-v1'
d=json.loads((O/'records.json').read_text());v=json.loads((O/'validation.json').read_text())
assert v['passed'] and d['failures']==0 and len(d['records'])==8
C=P/'release-continue-captures';C.mkdir(exist_ok=True);hashes={}
for gear in ['bare','helmet']:
 board=Image.new('RGB',(800,260),'#182932');draw=ImageDraw.Draw(board)
 for pair,phase in enumerate(['before','released']):
  rows=[r for r in d['records'] if r['name'].startswith(gear+'-'+phase+'-')];assert len(rows)==2
  root=rows[0]['foot'];x=255+(root[0]-7680)*398/384;y=287+(root[1]-8064)*398/384
  for j,r in enumerate(rows):
   col=pair*2+j
   for kind in ['room','source']:
    name=r['name']+'-'+kind+'.png';shutil.copy2(O/name,C/name);hashes[name]=hashlib.sha256((C/name).read_bytes()).hexdigest()
   im=Image.open(C/(r['name']+'-room.png')).convert('RGB');board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(col*200+10,40))
   draw.text((col*200+10,8),phase+' / '+('saved' if j==0 else 'restored'),fill='#dde8e9')
   draw.text((col*200+10,224),'owned='+str(r['caseOwned'])+' embedded='+str(r['embedded']),fill='#dde8e9')
   draw.text((col*200+10,241),r['state']+' / '+r['direction'],fill='#dde8e9')
 board.save(P/(gear+'-release-continue-review.png'))
(P/'release-continue-capture-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
(P/'release-continue-review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill release-boundary Continue</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:850px}figure{margin:25px 0;overflow:auto}img{max-width:none}</style><h1>Bill · release-boundary Continue</h1><p>Four actual disk/fresh-main restores: both gears just before inferred release frame8 and immediately after it. Exact source, physical foot, clock, floor presence and 30 future actor/player/source/case ticks checked. Original captures copied unchanged. Floor helpers explicitly staged; normal production admission and continuous motion remain open.</p><figure><img src="bare-release-continue-review.png"></figure><figure><img src="helmet-release-continue-review.png"></figure>''',encoding='utf-8')
print('Four boundary Continue pairs / 16 original captures retained.')
