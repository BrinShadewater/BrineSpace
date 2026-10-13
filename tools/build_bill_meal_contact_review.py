from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'output/bill-meal-counter-contact-candidate-v1'
d=json.loads((OUT/'contacts.json').read_text());rows=[r for r in d['captures'] if r['action'].endswith('enter') and r['pose']==3]
board=Image.new('RGB',(800,((len(rows)+3)//4)*330),(34,52,62));draw=ImageDraw.Draw(board)
for i,r in enumerate(rows):
 im=Image.open(OUT/r['screenshot']);box=(505,535,635,670) if r['station']['prop']=='library/sp-galley-2' else (270,295,400,435)
 # Native screenshot detail only, not character-source editing or fake contact.
 crop=im.crop(box);crop.thumbnail((195,280));x=(i%4)*200;y=(i//4)*330;board.paste(crop,(x,y+40));draw.text((x+3,y+4),f"q{r['rotation']} {r['station']['facing']} {r['action']}",fill='white')
board.save(OUT/'contact-detail-review.png')
html='<!doctype html><meta charset="utf-8"><title>Bill meal counter contact audit</title><style>body{font:16px system-ui;background:#152027;color:#e6eff1;margin:24px}img{max-width:100%;image-rendering:auto}p{max-width:80ch}</style><h1>Bill meal counter contact audit</h1><p>Actual copied owner layouts and normal galley stations, with static staged art injected for pose review. Green navigation/chooser checks do not establish hand/worktop contact. Activity phase clocks are not installed.</p>'
for r in rows:html+=f"<p>rotation {r['rotation']} · {r['station']['facing']} · {r['station']['prop']} · {r['action']} pose {r['pose']}</p><img src='{r['screenshot']}'>"
(OUT/'index.html').write_text(html,encoding='utf-8')
print('Contact review: %d actual reach captures; screenshot crops only'%len(rows))
