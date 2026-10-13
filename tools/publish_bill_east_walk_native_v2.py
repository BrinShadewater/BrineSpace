"""Retain scoped native evidence and fixed station crops for visual review."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,shutil,hashlib
R=Path(__file__).resolve().parents[1];O=R/'output/bill-east-walk-world-v2';D=R/'character/bill-east-walk-master-full-v1';N=D/'native'
v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed']
N.mkdir(exist_ok=False)
report=json.loads((O/'report.json').read_text(encoding='utf-8'))
for name in ['report.json','validation.json','inputs-before.json']:
 shutil.copyfile(O/name,N/name)
for c in report['captures']:
 for key in ['worldFile','sourceFile']:shutil.copyfile(O/c[key],N/c[key])
pages=[]
for page,start in enumerate(range(0,len(report['captures']),10)):
 batch=report['captures'][start:start+10];b=Image.new('RGB',(1400,620),'#17252d');draw=ImageDraw.Draw(b)
 draw.text((12,10),'Actual furnished station · revised above / selected below · prescribed source samples',fill='white')
 for i,c in enumerate(batch):
  x=i//2*280;y=45+i%2*280
  im=Image.open(N/c['worldFile']).crop((495,170,635,305)).resize((280,270),Image.Resampling.NEAREST);b.paste(im,(x,y));draw.text((x+6,y-14),f"{c['key']} {c['slot']} {c['variant']}",fill='white')
 path=N/f'world-review-{page}.png';b.save(path);pages.append(path.relative_to(D).as_posix())
proof=dict(nativePagesReviewed=False,checks=v['checks'],failures=v['failures'],pages=pages,normalAdmission=False,fullVisualAcceptance=False,scope=report['scope'],sourceSoleDepthAccepted=True,ownerChanges=v['ownerChanges'],inputChanges=v['inputChanges'])
(N/'verification.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(checks=v['checks'],captures=len(report['captures']),pages=pages)))
