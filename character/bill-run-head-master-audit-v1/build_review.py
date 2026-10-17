"""Expose head/neck changes at equal anatomical density without per-pose fitting."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];audit=json.loads((R/'character/bill-selected-source-audit-2026-10-01-locomotion-v3/source-inventory.json').read_text());records=[]
board=Image.new('RGB',(3072,3072),(34,52,62));draw=ImageDraw.Draw(board)
for g,gear in enumerate(['bare','helmet']):
 for n,direction in enumerate(['east','west','south','north']):
  row=g*4+n;src=audit['selectedStateSources'][gear]['run-'+direction];idle=audit['selectedStateSources'][gear]['idle-'+direction]
  master=R/f'character/bill-seated-{"helmet-" if gear=="helmet" else ""}{direction}-coherent-v1/frames/sit-down-{direction}/000.png'
  choices=[(master,[128,224],148,'Master'),(R/idle['sourceFiles'][0][6:],idle['pivot'],idle['standingHeight'],'Selected idle')]+[(R/f[6:],src['pivot'],src['standingHeight'],'Run '+str(i)) for i,f in enumerate(src['sourceFiles'])]
  for col,(f,pivot,height,caption) in enumerate(choices):
   im=Image.open(f).convert('RGBA');assert height==148,'No per-pose fitting';plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,(round(128-pivot[0]),round(224-pivot[1])));a=np.array(plane);y,x=np.indices(a.shape[:2]);head=(a[:,:,3]>180)&(x>=100)&(x<166)&(y>=55)&(y<105);top=int(np.where(head)[0].min());crown=head&(y<top+14);yy,xx=np.where(crown)
   metrics={'crownY':top,'crownWidth':int(xx.max()-xx.min()+1),'crownAxisX':float(np.median(xx)),'file':f.relative_to(R).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
   records.append({'gear':gear,'direction':direction,'pose':caption,**metrics})
   crop=plane.crop((88,55,184,143)).resize((384,352),Image.Resampling.NEAREST);board.paste(crop,(col*384,row*384),crop);draw.text((col*384+12,row*384+355),gear+' '+direction+' '+caption+' w'+str(metrics['crownWidth']),fill='white')
board.save(P/'head-neck-review.png');(P/'source-review.json').write_text(json.dumps({'scope':'Native1:1 head/neck/shoulder source crops displayed4x nearest; crown14-row width is a diagnostic silhouette, not anatomical measurement or acceptance. All6 selected run phases, both profiles and cardinal directions. No per-pose scale/width normalization.','poses':records},indent=2)+'\n')
print(json.dumps({d:{'master':next(r['crownWidth'] for r in records if r['gear']=='bare' and r['direction']==d and r['pose']=='Master'),'runs':[r['crownWidth'] for r in records if r['gear']=='bare' and r['direction']==d and r['pose'].startswith('Run')]} for d in ['east','west','south','north']}))

