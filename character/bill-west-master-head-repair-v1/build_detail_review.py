from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
bank=ROOT/'character/bill-walk-west-master-repair-v2'
poses={q['frame']:bank/q['study'] for q in json.loads((bank/'bank-assessment.json').read_text())['poses']}
board=Image.new('RGBA',(1200,850),(31,35,40,255));d=ImageDraw.Draw(board);inputs={}
selected=json.loads((OUT/'review.json').read_text())['poses']
for col,i in enumerate([27,28,29,34,35]):
 key=f'bare-walk-{i:03}';version=2 if i==28 else 1
 prop=OUT/f'sources/{key}-proportion-v{version}.png'
 paths=[poses[i],prop,OUT/f'{key}-candidate.png']
 for row,(name,p) in enumerate(zip(['Original walk','Proportion correction','Detail candidate'],paths)):
  inputs[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest();im=Image.open(p).convert('RGBA');x=col*240;y=row*280
  revision=next(q['revision'] for q in selected if q['key']==key)
  d.text((x+8,y+10),f'{i:03} | {name}'+(f' v{revision}' if row==2 else ''),fill='white')
  crop=im.crop((100,60,170,130)).resize((210,210),Image.Resampling.NEAREST);board.alpha_composite(crop,(x+15,y+40))
board.save(OUT/'detail-family-review.png')
(OUT/'detail-family-review.json').write_text(json.dumps({'frozenInputs':inputs,'scope':'Fixed head/collar/shoulder crops, original vs proportion vs detail candidates. Detail edits remain provisional; no isolated bank installed.','normalAdmission':False},indent=2)+'\n',encoding='utf-8')
print('Built five-pose original/proportion/detail comparison;15 frozen inputs.')
