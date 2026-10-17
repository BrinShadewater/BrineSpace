"""Compare complete-walk representatives to master and adjacent water poses."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
inputs={}
def read(p):
 inputs[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
 return Image.open(p).convert('RGBA')
def common(im):
 if im.size==(256,256):
  c=Image.new('RGBA',(352,320));c.alpha_composite(im,(32,0));return c
 assert im.size==(352,320);return im
selection=OUT/'review.json';inputs[str(selection)]=hashlib.sha256(selection.read_bytes()).hexdigest()
q=json.loads(selection.read_text(encoding='utf-8'))
assert len([p for p in q['poses'] if p['key'].startswith('bare-walk-')])==48
items=[('Original master / sole registered',read(ROOT/'character/bill-west-master-head-audit-v1/master-sole-registered.png'))]
for n in [0,12,24,28,34,37,47]:
 items.append((f'Provisional walk{n:03}',common(read(OUT/f'bare-walk-{n:03}-candidate.png'))))
for name in ['ready','rise']:
 items.append((f'Water {name} / prior joint source',common(read(ROOT/f'character/bill-west-water-joint-continuity-v1/bare-{name}-candidate.png'))))
board=Image.new('RGBA',(1760,1480),(31,35,40,255));d=ImageDraw.Draw(board)
for i,(label,im) in enumerate(items):
 x=(i%5)*352;y=(i//5)*740
 d.text((x+8,y+10),label,fill='white');board.alpha_composite(im,(x,y+35))
 d.line((x+100,y+259,x+250,y+259),fill=(65,180,195))
 d.text((x+8,y+375),'Fixed head/collar window x3',fill='white')
 board.alpha_composite(im.crop((120,55,200,135)).resize((240,240),Image.Resampling.NEAREST),(x+55,y+405))
 d.text((x+8,y+690),'H148 / pivot160,224 / no part fitting',fill='white')
board.save(OUT/'walk-water-master-family-review.png')
report={'scope':'Master, seven representative corrected walk poses and both prior water joint poses at original density. Fixed windows are diagnostics, not anatomical masks.',
 'frozenInputs':inputs,'labels':[x[0] for x in items],'normalAdmission':False,'nativeAcceptance':False,'fullVisualAcceptance':False}
(OUT/'family-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'{len(inputs)} frozen family inputs; ten whole sources compared.')
