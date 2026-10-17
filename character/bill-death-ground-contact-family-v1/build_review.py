from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-death-ground-contact-station-v1'
records=json.loads((O/'contacts.json').read_text())['records']
for contact,crop in [('counter',(495,520,640,665)),('aisle',(385,300,530,445))]:
 board=Image.new('RGB',(435,660),(34,52,62));draw=ImageDraw.Draw(board)
 for row,(d,gear) in enumerate((d,g) for d in ['north','south'] for g in [False,True]):
  for col,phase in enumerate(['before-kneel','entry','terminal']):
   item=next(r for r in records if r['contact']==contact and r['direction']==d and r['gear']==gear and r['phase']==phase)
   board.paste(Image.open(O/item['screenshot']).convert('RGB').crop(crop),(col*145,row*165+20));draw.text((col*145+2,row*165+2),d+(' gear ' if gear else ' bare ')+phase,fill='white')
 board.save(P/f'station-{contact}-review.png')
(P/'station-review.json').write_text(json.dumps({'status':'saved_contact_choice_candidate_review','captureBindings':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in O.glob('*.png')},'scope':'actual selection picks lateral at counter and original in aisle; fixture-facing and last kneel; physical footprint/wider joins pending'},indent=2)+'\n',encoding='utf-8')
(P/'station-review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill contact-aware collapse review</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:90ch}a{color:#80d4df}</style><h1>Bill — contact-aware collapse candidate</h1><p>Actual kill/room renderer selects lateral falls at the tested counter and original falls in the aisle. Both variants and their lowered entry phases survive production disk restoration. This is an explicitly loaded candidate family, not normal art selection or fresh-process Continue proof. Fine joins and wider physical placement remain open.</p><h2>Counter: lateral selected</h2><img src="station-counter-review.png"><h2>Aisle: original selected</h2><img src="station-aisle-review.png">''',encoding='utf-8')
print('Built48 hash-bound actual-choice captures and axial candidate review')
