from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent
original=Image.open(P/'edit-target.png').convert('RGBA');raw=Image.open(P/'raw-edited-v1.png').convert('RGBA')
assert original.width*raw.height==raw.width*original.height,'Aspect ratio changed'
# One complete-atlas canvas resample; never per-pose density or registration.
candidate=raw.resize(original.size,Image.Resampling.LANCZOS)
rows=[];boards=[]
for page in range(4):
 board=Image.new('RGB',(2048,600),'#202a30');draw=ImageDraw.Draw(board)
 for col in range(8):
  i=page*8+col;box=(col*256,page*256,(col+1)*256,(page+1)*256)
  source=original.crop(box);edited=candidate.crop(box);a=np.array(source);b=np.array(edited)
  masks=[a[:,:,3]>200,b[:,:,3]>200];geometry=[]
  for mask in masks:
   y,x=np.where(mask);top=int(y.min());hx=np.where(mask[top:top+16])[1]
   geometry.append({'height':int(y.max()-y.min()+1),'floor':int(y.max()),'top':top,'headWidth':int(hx.max()-hx.min()+1),'headAxis':float((hx.max()+hx.min())/2)})
  union=masks[0]|masks[1];intersection=masks[0]&masks[1]
  row={'slot':i,'rawFrame':i+32,'source':geometry[0],'edited':geometry[1],'opaqueSilhouetteIoU':float(intersection.sum()/union.sum()),'opaqueMaskChangedPixels':int((masks[0]^masks[1]).sum())};rows.append(row)
  dest=P/f'diagnostic-frames/{i:03}.png';dest.parent.mkdir(exist_ok=True);edited.save(dest)
  board.paste(source,(col*256,22),source);board.paste(edited,(col*256,310),edited)
  draw.text((col*256+3,3),f'{i} original H{geometry[0]["height"]} head{geometry[0]["headWidth"]}',fill='white')
  draw.text((col*256+3,291),f'edit H{geometry[1]["height"]} head{geometry[1]["headWidth"]} IoU{row["opaqueSilhouetteIoU"]:.3f}',fill='white')
 dest=P/f'geometry-review-{page}.png';board.save(dest);boards.append(dest.name)
report={'generationId':'8cad1051-1782-4150-b651-82081eef6489','rawSize':list(raw.size),'targetSize':list(original.size),'wholeAtlasScale':original.width/raw.width,'rows':rows,'heightRange':[min(r['edited']['height'] for r in rows),max(r['edited']['height'] for r in rows)],'headWidthRange':[min(r['edited']['headWidth'] for r in rows),max(r['edited']['headWidth'] for r in rows)],'meanSilhouetteIoU':float(np.mean([r['opaqueSilhouetteIoU'] for r in rows])),'boards':boards,'scope':'Canvas-normalized whole32-frame source edit geometry comparison, no per-pose resizing/registration, no RGB/alpha/anatomy fixes. Diagnostic only; no native or source acceptance.'}
(P/'geometry-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='rows'}))
