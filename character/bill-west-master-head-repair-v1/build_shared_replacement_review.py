"""Rebuild retained shared-study versus current-source comparisons."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
preferred={p['key']:p for p in json.loads((OUT/'review.json').read_text())['poses']}
board=Image.new('RGBA',(1960,1040),(31,35,40,255));d=ImageDraw.Draw(board);inputs={}
for col,frame in enumerate([12,13,14,15,25,31,32]):
 key=f'bare-walk-{frame:03}';first=OUT/f'generation-provenance-{key}-v1.json'
 original=Path(json.loads(first.read_text())['sourcePath'])
 current=OUT/f"generation-provenance-{key}-v{preferred[key]['revision']}.json"
 paths=[original,OUT/f'{key}-shared-v1-candidate.png',OUT/f'{key}-candidate.png']
 for row,(label,path) in enumerate(zip(['Original','Prior shared-sheet study','Current single-target study'],paths)):
  im=Image.open(path).convert('RGBA');assert im.size==(256,256);inputs[str(path)]=sha(path)
  x=col*245;y=row*205;d.text((x+8,y+8),f'{frame:03} | {label}',fill='white')
  board.alpha_composite(im.crop((105,65,155,115)).resize((150,150),Image.Resampling.NEAREST),(x+45,y+40))
 im=Image.open(paths[2]).convert('RGBA');d.text((col*245+8,640),f'{frame:03} | whole candidate',fill='white');board.alpha_composite(im,(col*245,675))
 for receipt in (first,current):inputs[str(receipt)]=sha(receipt)
master=OUT.parent/'bill-west-master-head-audit-v1/master-sole-registered.png';inputs[str(master)]=sha(master);im=Image.open(master).convert('RGBA')
d.text((1723,8),'Original master | fixed density',fill='white');board.alpha_composite(im.crop((137,65,187,115)).resize((150,150),Image.Resampling.NEAREST),(1760,40))
d.text((1723,640),'Original master | whole reference',fill='white');board.alpha_composite(im,(1680,675))
d.text((8,1000),'Fixed source windows only; no anatomy segmentation or fitting. All preferred source revisions remain provisional; detail, grade and motion acceptance pending.',fill='white')
board.save(OUT/'shared-to-single-review.png')
(OUT/'shared-to-single-review.json').write_text(json.dumps({'frames':[12,13,14,15,25,31,32],'inputs':inputs,'normalAdmission':False,'fullVisualAcceptance':False},indent=2)+'\n',encoding='utf-8')
print(f'{len(inputs)} frozen method comparison inputs')
