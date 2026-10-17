from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;D=P/'browser-review';rows=json.loads((D/'playback.json').read_text(encoding='utf-8'))
selected=[dict(speed='paused',pose=0,file='initial.png')]
for pose in range(1,9):
 candidates=[r for r in rows if r['speed']=='quarter' and r['pose']==pose];assert candidates
 selected.append(candidates[len(candidates)//2])
board=Image.new('RGB',(1500,760),'#182932');draw=ImageDraw.Draw(board)
for i,r in enumerate(selected):
 im=Image.open(D/r['file']);assert im.size==(1265,712)
 crop=im.crop((8,166,483,690)).resize((285,314),Image.Resampling.LANCZOS)
 x=(i%5)*300;y=(i//5)*380;board.paste(crop,(x,y+24));draw.text((x+6,y+6),f"{r['speed']} sampled label{r['pose']}",fill='white')
board.save(D/'sampled-motion-board.png')
report=dict(samples=len(rows),quarterSamples=sum(r['speed']=='quarter' for r in rows),normalSamples=sum(r['speed']=='normal' for r in rows),quarterLabels=sorted({r['pose'] for r in rows if r['speed']=='quarter'}),normalLabels=sorted({r['pose'] for r in rows if r['speed']=='normal'}),screenshotSHA256={r['file']:hashlib.sha256((D/r['file']).read_bytes()).hexdigest() for r in rows},scope='Actual source-browser Playonce controls;33quarter screenshots cover observed labels1..8,6normal screenshots cover4..8. Initial0 separately paused. AX sampled before screenshot may cross holds, no source-phase pixel binding or complete normal-speed chronology/duration/native acceptance. Same fixed screenshot crop for every sample.',visualReview='Pending sampled board inspection.')
(D/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(D/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>South sampled motion</title><style>body{background:#182932;color:#ddd;font:17px sans-serif}img{max-width:100%}</style><h1>Bill South sampled playback</h1><p>'+report['scope']+'</p><img src="sampled-motion-board.png">',encoding='utf-8')
print(json.dumps(dict(samples=len(rows),quarterLabels=report['quarterLabels'],normalLabels=report['normalLabels'])))
