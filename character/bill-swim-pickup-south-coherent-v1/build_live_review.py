from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-pickup-south-live-boundary-v1'
timeline=json.loads((OUT/'timeline.json').read_text(encoding='utf-8'))
for row in timeline:
 files=sorted((OUT/row['name']).glob('*.png'));images=[Image.open(p).convert('RGB') for p in files]
 images[0].save(P/(row['name']+'-live.gif'),save_all=True,append_images=images[1:],duration=[20 if i%3!=2 else 10 for i in range(len(images))],loop=0)
board=Image.new('RGB',(1260,720),(29,43,51));d=ImageDraw.Draw(board)
for j,row in enumerate(timeline):
 samples=row['samples'];last=int(row['firstReturn']['tick']);indices=[max(0,next(i for i,s in enumerate(samples) if s['tick']==last)-1),next(i for i,s in enumerate(samples) if s['tick']==last),next(i for i,s in enumerate(samples) if s['tick']==last+1)]
 for column,i in enumerate(indices):
  im=Image.open(OUT/row['name']/f'{i:03}.png');board.paste(im,(column*420,j*180))
board.save(P/'live-return-audit.png')
paths=[OUT/'timeline.json',OUT/'validation.json',OUT/'native.log',ROOT/'tests/test_bill_pickup_south_live_boundary.gd',ROOT/'scripts/grid_canvas.gd',ROOT/'scripts/crew_expedition.gd',ROOT/'scripts/bill_npc.gd']
for folder in [P,P.parent/'bill-swim-pickup-helmet-south-coherent-v1',P.parent/'bill-salvage-south-coherent-v1',P.parent/'bill-salvage-helmet-south-coherent-v1']:
 manifest=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));paths.append(folder/'manifest.json');paths.extend(folder/file for state in manifest['states'] for file in state['frameFiles'])
(P/'live-boundary-evidence.json').write_text(json.dumps({'validation':json.loads((OUT/'validation.json').read_text(encoding='utf-8')),'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'scope':'actual expedition.advance and grid renderer;candidate art injection;direct isolated work start,not full exterior journey'},indent=2)+'\n',encoding='utf-8')
html='<!doctype html><meta charset="utf-8"><title>Bill live work return boundary</title><style>body{background:#152027;color:#e6eff1;font:16px system-ui;margin:20px}section{display:inline-block;margin:10px}img{display:block;image-rendering:auto}a{color:#92d9dc}</style><h1>Bill — live pickup and recall</h1><p>Actual expedition controller and grid renderer. 82px native contact samples; candidate South art injected. Nominal pickup keeps cargo; early recall returns empty and stays prone. Source atlas preview: <a href="index.html">pickup poses</a>.</p>'
for row in timeline:html+=f'<section><h2>{row["name"]}</h2><img width="630" height="270" src="{row["name"]}-live.gif"></section>'
(P/'live-review.html').write_text(html,encoding='utf-8')
