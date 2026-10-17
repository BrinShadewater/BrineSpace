from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-floor-case-finish-priority-v1'
d=json.loads((O/'records.json').read_text());v=json.loads((O/'validation.json').read_text());assert v['passed'] and d['failures']==0 and len(d['records'])==40
C=P/'finish-priority-captures';C.mkdir(exist_ok=True);hashes={};boards=[]
for event in ['fire','flood','gear','death','removal']:
 for gear in ['bare','helmet']:
  board=Image.new('RGB',(800,255),'#182932');draw=ImageDraw.Draw(board)
  for pair,phase in enumerate([10,39]):
   key=f'{event}-{gear}-{phase}';rows=[r for r in d['records'] if r['name'].startswith(key+'-')];assert len(rows)==2
   root=rows[0]['foot'];x=255+(root[0]-7680)*398/384;y=287+(root[1]-8064)*398/384
   for j,row in enumerate(rows):
    col=pair*2+j
    for kind in ['room','source']:
     name=row['name']+'-'+kind+'.png';shutil.copy2(O/name,C/name);hashes[name]=hashlib.sha256((C/name).read_bytes()).hexdigest()
    im=Image.open(C/(row['name']+'-room.png')).convert('RGB');board.paste(im.crop((round(x-90),round(y-145),round(x+90),round(y+35))),(col*200+10,35))
    draw.text((col*200+10,8),str(phase)+' / '+('pre-event' if j==0 else 'post-event'),fill='#dde8e9')
    draw.text((col*200+10,220),'owned='+str(row['caseOwned'])+' exit='+str(row['finishActive']),fill='#dde8e9')
    draw.text((col*200+10,238),'removed room' if row.get('roomRemoved') else row['state']+' / '+row['direction'],fill='#dde8e9')
  name=f'{event}-{gear}-finish-priority-review.png';board.save(P/name);boards.append(name)
html='''<!doctype html><meta charset="utf-8"><title>Bill set-down priority takeover</title><style>body{background:#182932;color:#dde8e9;font:15px system-ui;margin:22px}p{max-width:900px}figure{overflow:auto;margin:24px 0}img{max-width:none}</style><h1>Bill · staged exit priority takeover</h1><p>20 actual event takeovers during the ordinary North service-loss exit, both gears before and after inferred release. Fire refresh, room flooding with real water/air medium update, public gear setter, mortality and controlled actual room-array/occupied removal with topology rebuild. Fifteen future exit/floor-state ticks checked; original captures retained unchanged.</p><p>Priority replaces finite exit immediately. Pre-release held-case disappearance remains unresolved; released case stays owned until its room is removed. Flood overlays obscure Bill: these captures establish takeover checks but do not establish native pose visibility, matte-grade/detail or contact acceptance. Fire shows dispatch, death shows initial fall; no complete escape/fall, normal selection, Continue or continuous-motion acceptance.</p><p>Initial run failed flood checks because fixture skipped the world water/air update. Original failed interval/captures retained; corrected fixture calls the actual medium update before actor update. No assertions or production behavior weakened. Second run passed technically but bare room removal caused actual unprotected exterior death and a run-report overlay that persisted into later cases. That interval is retained; final removal cases each use a fresh scene. Bare removal after-captures still show the legitimate run-report backdrop, so visual disappearance is unproven there; retained room-canvas removal is checked separately.</p>'''
for name in boards:html+=f'<h2>{name.removesuffix("-finish-priority-review.png")}</h2><figure><img src="{name}"></figure>'
html+='<p>Helmeted room removal still draws Bill through the global actor fallback outside the removed room. The guard establishes absence of the owning retained room canvas, not disappearance of all actor drawing. Outside pose/contact and medium handling remain unaccepted.</p>'
(P/'finish-priority-review.html').write_text(html,encoding='utf-8')
(P/'finish-priority-review-evidence.json').write_text(json.dumps({'validation':v,'checks':d['checks'],'boards':boards,'captureHashes':hashes,'scope':d['scope']},indent=2)+'\n')
print('20 pairs / 40 native presentations / 80 original captures / 10 boards retained.')
