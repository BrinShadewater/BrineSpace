from pathlib import Path
import numpy as np,json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
files=[P.parent/'bill-seated-south-coherent-v1/frames/sit-down-south/000.png']+[P/f'frames/drink-south/{i:03}.png' for i in range(7)]
rows=[]
for f in files:
 a=np.array(Image.open(f).convert('RGBA'));y,x=np.where(a[:,:,3]>180);bands={}
 for name,lo,hi in [('hair',76,85),('head',76,100),('legs',175,195),('boots',210,224)]:
  bx=x[(y>=lo)&(y<=hi)];bands[name]=[int(bx.min()),int(bx.max())] if len(bx) else []
 rows.append({'file':f.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'crown':int(y.min()),'sole':int(y.max()),'bands':bands})
(P/'master-comparison.json').write_text(json.dumps({'scope':'alpha bands support visual review; not full design/material/contact proof','frames':rows},indent=2)+'\n')
print(json.dumps({'master':rows[0],'frame0':rows[1],'crownRange':[min(r['crown'] for r in rows[1:]),max(r['crown'] for r in rows[1:])]}))
