from pathlib import Path

import json,hashlib

import numpy as np

from PIL import Image,ImageDraw

P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-normal-continue-v1'

d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed'] and not d['failures'] and len(d['records'])==6

sections=[];pairs=[]

for helmet in [False,True]:

 group=[r for r in d['records'] if r['helmet']==helmet];board=Image.new('RGB',(600,720),'#22343e');draw=ImageDraw.Draw(board)

 for row,r in enumerate(group):

  name=r['name'];before=np.array(Image.open(O/(name+'-before-source.png')).convert('RGBA'));after=np.array(Image.open(O/(name+'-after-source.png')).convert('RGBA'));assert np.array_equal(before,after)

  x=255+(r['foot'][0]-7680)*398/384;y=287+(r['foot'][1]-8064)*398/384

  for col,phase in enumerate(['before','after']):

   native=Image.open(O/(name+'-'+phase+'-room.png')).convert('RGB');crop=native.crop((round(x)-75,round(y)-130,round(x)+75,round(y)+50));board.paste(crop,(col*300,row*240+30))

   source=Image.open(O/(name+'-'+phase+'-source.png')).convert('RGBA').resize((142,142),Image.Resampling.LANCZOS);board.paste(source,(col*300+150,row*240+55),source)

   draw.text((col*300+5,row*240+5),f'{r["phase"]} {phase}',fill='#dde8e9');draw.text((col*300+5,row*240+214),'NATIVE ROOM     SOURCE82',fill='#dde8e9')

  pairs.append({'name':name,'wholeSourceRGBAEqual':True,'beforeSourceSha256':hashlib.sha256((O/(name+'-before-source.png')).read_bytes()).hexdigest(),'afterSourceSha256':hashlib.sha256((O/(name+'-after-source.png')).read_bytes()).hexdigest()})

 tag='helmet' if helmet else 'bare';board.save(P/(tag+'-continue-review.png'));links=' '.join(f'<a href="../../output/bill-carry-normal-continue-v1/{r["name"]}-{phase}-room.png">{r["phase"]} {phase}</a>' for r in group for phase in ['before','after']);sections.append(f'<h2>{tag}</h2><p>Original station captures: {links}</p><img src="{tag}-continue-review.png">')

print('Six exact fresh cardinal pairs packaged')



(P/'continue.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill carrying save and resume</title><style>body{background:#182932;color:#dde8e9;font:16px system-ui;margin:24px}img{max-width:100%}</style><h1>Bill - selected carrying save and resume</h1><p>Before saving on the left, restored in a fresh scene on the right. Each pair shows the actual room and submitted source.</p>'+''.join(sections),encoding='utf-8')

(P/'continue-evidence.json').write_text(json.dumps({'native':v,'checks':d['checks'],'scope':d['scope'],'pairs':pairs,'normalTitleSelectionChanged':True},indent=2)+'\n')

