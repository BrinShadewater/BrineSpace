from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-death-ground-fresh-continue-v1'
report=json.loads((O/'validation.json').read_text());assert report['nativePassed'] and report['processes']==16
bindings={}
for contact,crop in [('counter',(495,520,640,665)),('aisle',(385,300,530,445))]:
 board=Image.new('RGB',(290,660),(34,52,62));draw=ImageDraw.Draw(board)
 for row,(d,g) in enumerate((d,g) for d in ['north','south'] for g in ['bare','helmet']):
  for col,phase in enumerate(['mid','terminal']):
   f=O/f'{contact}-{d}-{g}-{phase}.png';board.paste(Image.open(f).convert('RGB').crop(crop),(col*145,row*165+20));draw.text((col*145+2,row*165+2),d+' '+g+' '+phase,fill='white');bindings[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
 board.save(P/f'continued-{contact}-review.png')
(P/'continue-review.json').write_text(json.dumps({'status':'normal_loader_fresh_title_continue_reviewed','captureBindings':bindings,'scope':'16 separate fresh engine processes with actual title/loading Continue buttons; mid/terminal two contacts/two gears/axial headings; fine joins and wider placement pending'},indent=2)+'\n',encoding='utf-8')
(P/'continue-review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Bill normal Continue review</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:24px}img{max-width:100%}p{max-width:90ch}</style><h1>Bill — normal runtime and fresh Continue</h1><p>Each panel comes from a separate engine process using the actual title Continue button and loading transmission Continue. Normal artwork loader, saved variant and entry phase, paused exact mid-fall/terminal pixels. Counter chooses lateral; aisle retains original. Fine transitions and wider physical placement still need review.</p><h2>Counter</h2><img src="continued-counter-review.png"><h2>Aisle</h2><img src="continued-aisle-review.png">''',encoding='utf-8')
print('Built16 hash-bound fresh Continue room crops at native scale')
