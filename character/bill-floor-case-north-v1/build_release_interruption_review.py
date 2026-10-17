"""Retain original interruption captures and show fixed-root native comparisons."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-release-world-v1'
d=json.loads((O/'records.json').read_text());v=json.loads((O/'validation.json').read_text())
assert v['passed'] and d['failures']==0 and len(d['records'])==48
C=P/'release-captures';C.mkdir(exist_ok=True);hashes={}
for event in ['service','fire','gear','death']:
 for gear in ['bare','helmet']:
  board=Image.new('RGB',(1200,260),'#182932');draw=ImageDraw.Draw(board)
  for pair,phase in enumerate(['before','after','late']):
   rows=[r for r in d['records'] if r['name'].startswith(f'{event}-{gear}-{phase}-')];assert len(rows)==2
   root=rows[0]['foot'];x=255+(root[0]-7680)*398/384;y=287+(root[1]-8064)*398/384
   for j,r in enumerate(rows):
    col=pair*2+j
    for kind in ['room','source']:
     name=r['name']+'-'+kind+'.png';shutil.copy2(O/name,C/name)
     hashes[name]=hashlib.sha256((C/name).read_bytes()).hexdigest()
    im=Image.open(C/(r['name']+'-room.png')).convert('RGB')
    board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(col*200+10,40))
    draw.text((col*200+10,8),phase+' / '+('pre-event' if j==0 else 'post-event'),fill='#dde8e9')
    draw.text((col*200+10,224),'owned='+str(r['caseOwned'])+' embedded='+str(r['embedded']),fill='#dde8e9')
    draw.text((col*200+10,241),r['state']+' / '+r['direction'],fill='#dde8e9')
  board.save(P/f'release-{event}-{gear}-review.png')
html='''<!doctype html><meta charset="utf-8"><title>Bill interrupted set-down</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:900px}figure{margin:25px 0;overflow:auto}img{max-width:none}</style><h1>Bill · staged interrupted set-down</h1><p>24 real priority-event cases: service suspension, fire dispatch, public helmet changes and mortality. Both equipment variants at 0.32, 0.39 and 0.55 seconds into unload. Native crops retain a fixed pre-event physical root; all 96 original source/room captures retained unchanged.</p><p>Release frame 8 (0.36 seconds) is an inferred staged cue. Ground contact begins at frame 5. Ownership and visibility are separate: the standalone case is suppressed while the source already draws it. No normal production selection or complete continuous-motion acceptance. Before-release service loss still drops the held-case presentation; an authored return remains necessary.</p>'''
for event in ['service','fire','gear','death']:
 for gear in ['bare','helmet']:
  html+=f'<h2>{event} · {gear}</h2><figure><img src="release-{event}-{gear}-review.png"></figure>'
(P/'release-interruption-review.html').write_text(html,encoding='utf-8')
(P/'release-capture-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
print('24 pairs / 96 unchanged captures / 8 native boards retained.')
