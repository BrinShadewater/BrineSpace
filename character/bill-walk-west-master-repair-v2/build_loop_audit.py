from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
bank=json.loads((OUT/'bank-assessment.json').read_text(encoding='utf-8'))
assert [r['frame'] for r in bank['poses']]==list(range(48))
board=Image.new('RGB',(1536,1680),(23,42,51));draw=ImageDraw.Draw(board);rows=[]
def bounds(arr,box):
 lab,n=label(arr[:,:,3]>=180);counts=np.bincount(lab.ravel());mask=lab==int(counts[1:].argmax()+1)
 x,y,x1,y1=box;ys,xs=np.where(mask[y:y1,x:x1]);return [int(xs.min()+x),int(ys.min()+y),int(xs.max()+x+1),int(ys.max()+y+1)]
for r in bank['poses']:
 n=r['frame'];old=Image.open(ROOT/f'character/bill-walk-west-material-v1/frames/bare/walk-west/{n:03}.png').convert('RGBA');new=Image.open(OUT/r['study']).convert('RGBA')
 row={'frame':n,'scope':'Alpha180 main-component window bounds; not anatomical landmarks or acceptance'}
 for name,box in [('head',[105,65,145,108]),('glove',[95,130,150,164]),('boots',[70,197,180,232])]:
  a=bounds(np.array(old),box);b=bounds(np.array(new),box);row[name]={'selected':a,'edited':b,'delta':[v-u for u,v in zip(a,b)]}
 rows.append(row)
 for k,(name,im) in enumerate([('Selected',old),('Edited',new)]):
  x=(n%12)*128;y=(n//12)*420+k*210
  draw.text((x+4,y+3),f'{n:03} {name}',fill='white')
  crop=im.crop((95,65,155,160)).resize((120,190),Image.Resampling.NEAREST);board.paste(crop,(x+4,y+20),crop)
board.save(OUT/'full-loop-head-review.png')
for half in range(2):board.crop((0,half*840,1536,(half+1)*840)).save(OUT/f'full-loop-head-review-{half+1}.png')
report={'status':'full_bare_source_coverage_continuity_pending','frames':48,'helmetFramesRemaining':48,'normalAdmission':False,'nativeAcceptance':False,'rows':rows,'maxAbsHeadWindowDelta':max(abs(v) for r in rows for v in r['head']['delta']),'maxAbsGloveWindowDelta':max(abs(v) for r in rows for v in r['glove']['delta']),'maxAbsBootWindowDelta':max(abs(v) for r in rows for v in r['boots']['delta'])}
(OUT/'full-loop-continuity-diagnostics.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
