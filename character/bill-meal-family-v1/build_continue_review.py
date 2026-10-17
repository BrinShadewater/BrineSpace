from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-meal-fresh-continue-v1'
report=json.loads((O/'validation.json').read_text());cases=json.loads((R/'output/bill-meal-continue-producer-v1/continue-cases.json').read_text())
assert report['nativePassed'] and report['processes']==20
board=Image.new('RGB',(1000,720),(34,52,62));draw=ImageDraw.Draw(board)
for i,item in enumerate(cases):
    image=Image.open(O/(item['id']+'.png'));box=(505,535,635,670) if item['station']['prop']=='library/sp-galley-2' else (270,295,400,435)
    crop=image.crop(box);x=(i%5)*200;y=(i//5)*180;board.paste(crop,(x+25,y+35));draw.text((x+4,y+3),item['id'],fill='white');draw.text((x+4,y+18),item['pose']+' '+str(round(item['timer'],3))+'s',fill='#bdd0d2')
board.save(P/'continued-contact-review.png')
html='<!doctype html><meta charset="utf-8"><title>Bill meal fresh Continue review</title><style>body{font:16px system-ui;background:#14232b;color:#d1d9dc;padding:24px}img{max-width:100%}p{max-width:90ch}</style><h1>Bill · Fresh Continue meal review</h1><p>Twenty independent title-screen and loading-transmission Continue flows. Two actual galley contacts, bowl/cup draw, use, stow, partial draw cancellation and loop cancellation. Exact saved source pixels, timer, retained object/pose, physical contact and hunger validated. Crops below retain native screenshot pixels. All cases land paused; resumed journeys and broader hazard/gear interruptions remain separate.</p><img src="continued-contact-review.png">'
(P/'continue-review.html').write_text(html,encoding='utf-8')
print('Built20 actual fresh-Continue native contact crops')
