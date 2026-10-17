from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-finish-continue-v1'
d=json.loads((O/'records.json').read_text());v=json.loads((O/'validation.json').read_text());assert v['passed'] and d['failures']==0 and len(d['records'])==12
C=P/'finish-continue-captures';C.mkdir(exist_ok=True);hashes={}
for gear in ['bare','helmet']:
 board=Image.new('RGB',(1200,255),'#182932');draw=ImageDraw.Draw(board)
 for pair,phase in enumerate(['early','pre-release','released']):
  key=gear+'-'+phase;rows=[r for r in d['records'] if r['name'].startswith(key+'-')];assert len(rows)==2
  root=rows[0]['foot'];x=255+(root[0]-7680)*398/384;y=287+(root[1]-8064)*398/384
  for j,row in enumerate(rows):
   col=pair*2+j
   for kind in ['room','source']:
    name=row['name']+'-'+kind+'.png';shutil.copy2(O/name,C/name);hashes[name]=hashlib.sha256((C/name).read_bytes()).hexdigest()
   im=Image.open(C/(row['name']+'-room.png')).convert('RGB');board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(col*200+10,35))
   draw.text((col*200+10,8),phase+' / '+('saved' if j==0 else 'restored'),fill='#dde8e9')
   draw.text((col*200+10,220),'owned='+str(row['caseOwned'])+' exit='+str(row['finishActive']),fill='#dde8e9')
   draw.text((col*200+10,238),row['state']+' / '+row['direction'],fill='#dde8e9')
 board.save(P/f'{gear}-finish-continue-review.png')
html='''<!doctype html><meta charset="utf-8"><title>Bill finite-exit Continue</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:900px}figure{overflow:auto;margin:24px 0}img{max-width:none}</style><h1>Bill · staged service-loss exit Continue</h1><p>Six actual disk saves and fresh-main restores: both gears early, just before release and after release. Paired actor/player/source/clock/contact/floor metadata validated before mutation; altered shared source and malformed checkpoint rejection checked atomically. Original PNG captures retained unchanged.</p><p>Immediate pose/root/clock/case state, pause and 40 future actor/player/source/case ticks match. This is explicit staged wrapper/candidate admission using ordinary RunSave disk and station restore; not normal selection, Title/new-process Continue, retained older source-bank coverage, natural traffic or full continuous-motion acceptance. Terminal idle stance, flood visibility and early held-case priority disposition remain open.</p>'''
for gear in ['bare','helmet']:html+=f'<h2>{gear}</h2><figure><img src="{gear}-finish-continue-review.png"></figure>'
(P/'finish-continue-review.html').write_text(html,encoding='utf-8')
(P/'finish-continue-review-evidence.json').write_text(json.dumps({'validation':v,'checks':d['checks'],'captureHashes':hashes,'scope':d['scope']},indent=2)+'\n')
print('Six finite-exit Continue pairs / 12 native presentations / 24 original captures retained.')
