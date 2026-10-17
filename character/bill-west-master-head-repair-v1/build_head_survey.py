from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
bank=ROOT/'character/bill-walk-west-master-repair-v2'
poses=json.loads((bank/'bank-assessment.json').read_text())['poses']
report={'scope':'Full48 current source head/collar windows; fixed crop, no per-head fitting. Diagnostic silhouettes are not anatomy segmentation.','inputs':{},'normalAdmission':False}
selected={int(q['key'].split('-')[-1]) for q in json.loads((OUT/'review.json').read_text())['poses'] if q['key'].startswith('bare')}
board=Image.new('RGBA',(1440,1200),(31,35,40,255));d=ImageDraw.Draw(board)
partial=board.copy();pd=ImageDraw.Draw(partial)
for q in poses:
 i=q['frame'];p=bank/q['study'];report['inputs'][str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
 im=Image.open(p).convert('RGBA');x=(i%8)*180;y=(i//8)*200
 d.text((x+10,y+8),f'Current walk {i:02}',fill='white')
 board.alpha_composite(im.crop((105,65,155,115)).resize((150,150),Image.Resampling.NEAREST),(x+15,y+35))
 if i in selected:
  candidate=OUT/f'bare-walk-{i:03}-candidate.png';report['inputs'][str(candidate)]=hashlib.sha256(candidate.read_bytes()).hexdigest();im=Image.open(candidate).convert('RGBA')
 pd.text((x+10,y+8),f'{i:02} '+('corrected' if i in selected else 'unchanged'),fill='white')
 partial.alpha_composite(im.crop((105,65,155,115)).resize((150,150),Image.Resampling.NEAREST),(x+15,y+35))
board.save(OUT/'all48-current-head-review.png')
partial.save(OUT/'all48-partial-head-review.png');report['provisionalCorrections']=sorted(selected)
(OUT/'head-survey.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'Built before/partial full48 head surveys;{len(report["inputs"])} frozen inputs.')
