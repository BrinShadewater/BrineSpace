"""Review unmodified normal-loader Continue room crops; preserve scope."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-seated-north-selected-v1'
native=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert native['runtimePassed']
records=json.loads((O/'continuity.json').read_text(encoding='utf-8'))['records'];assert len(records)==8
board=Image.new('RGB',(1248,528),'#202a30');draw=ImageDraw.Draw(board);differences=[]
for row,gear in enumerate(('bare','helmet')):
 for col,elapsed in enumerate((.8,1.4,2.2,4.6)):
  name=f'{gear}-{str(elapsed).replace(".","-")}';crops=[]
  for index,version in enumerate(('before','after')):
   crop=Image.open(O/f'{name}-{version}.png').convert('RGB').crop((270,280,348,402));crops.append(crop)
   board.paste(crop.resize((156,244),Image.Resampling.NEAREST),(col*312+index*156,row*264+20))
   draw.text((col*312+index*156+3,row*264+3),f'{gear} {elapsed} {version}',fill='white')
  a=np.array(crops[0]);b=np.array(crops[1]);delta=np.abs(a.astype(int)-b.astype(int))
  differences.append({'gear':gear,'elapsed':elapsed,'roomCropEqual':crops[0].tobytes()==crops[1].tobytes(),'differentPixels':int(np.any(a!=b,axis=2).sum()),'maximumChannelDelta':int(delta.max())})
board.save(P/'normal-continue-contact.png')
(P/'room-crop-review.json').write_text(json.dumps({'scope':'unmodified native crops, eight actual disk/fresh-scene Continue pairs; exact source/calibration/contact/depth separately checked','comparisons':differences},indent=2)+'\n',encoding='utf-8')
(P/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld selected North seating</title><style>body{background:#202a30;color:#e1e7eb;font:16px system-ui;margin:24px}a{color:#8cc6e7}img{max-width:100%}p{max-width:80ch;line-height:1.5}</style><h1>Veld - selected North seating</h1><p>Original master-matched North sit and rise with subtle source-guided breathing. Fixed size, perspective, matte colours and directional helmet retained. Installed locally; final owner motion acceptance remains open.</p><h2>Actual lounge / fresh Continue</h2><p>Eight before/after pairs from the normal game loader. Same prescribed real chair contact; no candidate artwork injected. Pixel-size differences between facings are retained rather than stretching the seated pose.</p><img src="normal-continue-contact.png"><h2>Source breathing - actual 3.6-second timing</h2><img src="../veld-seated-north-breathing-source-v1/bare-breathing.gif" height="256"><img src="../veld-seated-north-breathing-source-v1/helmet-breathing.gif" height="256"><p><a href="../veld-seated-north-coherent-v1/index.html">Full sitting/rising source review</a> / <a href="HANDOFF.md">Evidence and remaining work</a></p>''',encoding='utf-8')
print(json.dumps({'pairs':len(differences),'equalRoomCrops':sum(d['roomCropEqual'] for d in differences),'maxChannelDelta':max(d['maximumChannelDelta'] for d in differences)}))
