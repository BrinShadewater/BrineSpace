from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;B=P/'browser-review'
rows=json.loads((B/'playback.json').read_text(encoding='utf-8'))
summary=[];board=Image.new('RGB',(2000,1760),'#182932');draw=ImageDraw.Draw(board)
for line,(gear,speed) in enumerate([('bare',4),('helmet',4),('bare',1),('helmet',1)]):
 group=[r for r in rows if r['gear']==gear and r['speed']==speed];assert group and group[-1]['phaseBeforeScreenshot']==7
 phases=sorted(set(r['phaseBeforeScreenshot'] for r in group))
 summary.append(dict(gear=gear,speed=speed,samples=len(group),observedAXPhasesBeforeScreenshot=phases,final=7))
 for col,phase in enumerate(phases):
  r=next(r for r in group if r['phaseBeforeScreenshot']==phase)
  image=Image.open(B/r['file']);assert image.size==(1265,712)
  # Same fixed screen crop and pixel scale in every sample; body position remains visible.
  crop=image.crop((115,220,365,630));x=col*250;y=line*440
  board.paste(crop,(x,y+25));draw.text((x+4,y+4),f'{gear} speed{speed} label{phase}',fill='white')
board.save(B/'advancing-browser-board.png')
report=dict(samples=len(rows),cases=summary,screenshotDimensions=[1265,712],screenCrop=[115,220,365,630],captureSHA256={r['file']:hashlib.sha256((B/r['file']).read_bytes()).hexdigest() for r in rows},scope='Actual UI Play once at normal/quarter speed, both gears. AX sampled immediately before screenshot can cross a hold boundary; no source-phase pixel binding. No full browser duration assertion; elapsed starts after click returns. Initial0 observed separately paused. Normal-speed phase coverage partial. Native exit/contact/master acceptance separate.',visualReview='Pending sampled progressing board inspection.')
(B/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(B/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Bill North exit moving review</title><style>body{background:#182932;color:#ddd;font:16px sans-serif}img{max-width:100%}</style><h1>Sampled North exit playback</h1><p>'+report['scope']+'</p><img src="advancing-browser-board.png"><pre>'+json.dumps(summary,indent=2)+'</pre>',encoding='utf-8')
print(json.dumps(dict(samples=len(rows),cases=summary)))
