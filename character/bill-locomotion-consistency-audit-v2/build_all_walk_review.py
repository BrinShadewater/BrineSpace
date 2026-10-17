"""Review every selected walk pose at common density, with native head crops."""
from pathlib import Path
import json,hashlib,math
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1]
inventory=R/'character/bill-selected-source-audit-2026-10-01-locomotion-v13/source-inventory.json';audit=json.loads(inventory.read_text());records=[]
block=(R/'scripts/grid_canvas.gd').read_text().split('func _load_major_bill_animations() -> void:',1)[1].split('\nfunc ',1)[0]
assert hashlib.sha256(block.encode()).hexdigest()==audit['loaderBlockSha256']
for direction in ['east','west','south','north']:
 for gear in ['bare','helmet']:
  s=audit['selectedStateSources'][gear]['walk-'+direction];manifest=R/s['manifest'];assert hashlib.sha256(manifest.read_bytes()).hexdigest()==audit['manifestSha256'][s['manifest']]
  master=R/f'character/bill-seated-{"helmet-" if gear=="helmet" else ""}{direction}-coherent-v1/frames/sit-down-{direction}/000.png'
  choices=[(master,[128,224],148,'Master')]+[(R/f[6:],s['pivot'],s['standingHeight'],str(i)) for i,f in enumerate(s['sourceFiles'])]
  board=Image.new('RGB',(1344,math.ceil(len(choices)/6)*224),(34,52,62));draw=ImageDraw.Draw(board);metrics=[]
  for i,(f,pivot,height,caption) in enumerate(choices):
   im=Image.open(f).convert('RGBA');scale=148/height
   assert scale==1,'Review must not silently rescale anatomy'
   plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,(round(128-pivot[0]),round(224-pivot[1])))
   x=(i%6)*224;y=(i//6)*224
   small=plane.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(x+41,y+16),small)
   crop=plane.crop((100,65,166,115)).resize((198,150),Image.Resampling.NEAREST)
   # Crop board allows careful head/neck viewing; full82px silhouette above stays registered.
   crop=crop.resize((158,120),Image.Resampling.NEAREST);board.paste(crop,(x+33,y+96),crop)
   draw.text((x+7,y+4),caption,fill='white')
   a=np.array(plane);yy,xx=np.indices(a.shape[:2]);alpha=(a[:,:,3]>180)&(xx>=100)&(xx<166)&(yy>=55)&(yy<105);ys=np.where(alpha)[0];top=int(ys.min());crown=alpha&(yy<top+14);xs=np.where(crown)[1]
   metrics.append({'pose':caption,'headTopY':top,'crown14Width':int(xs.max()-xs.min()+1),'file':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
  name=f'all-walk-{direction}-{gear}.png';board.save(P/name);records.append({'direction':direction,'gear':gear,'poses':len(s['sourceFiles']),'board':name,'diagnosticOnly':'Crown width includes perspective/occlusion; not anatomical acceptance','metrics':metrics})
(P/'all-walk-source-review.json').write_text(json.dumps({'scope':'Every current selected cardinal walk frame, common native density; diagnostic source review, no runtime/route or owner acceptance claim','inventorySha256':hashlib.sha256(inventory.read_bytes()).hexdigest(),'rows':records},indent=2)+'\n')
print(json.dumps([{'direction':r['direction'],'gear':r['gear'],'poses':r['poses'],'masterCrown':r['metrics'][0]['crown14Width'],'walkCrownRange':[min(x['crown14Width'] for x in r['metrics'][1:]),max(x['crown14Width'] for x in r['metrics'][1:])]} for r in records]))
