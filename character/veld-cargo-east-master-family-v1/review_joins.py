"""Read current declared East source endpoints at their physical pivot; no runtime mutation."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
selected={'bare':{'idle':'character/crew-runtime-matte-v1/veld/manifest.json','pickup':'character/veld-pickup-east-consistent-v1/bare-manifest.json','unload':'character/veld-unload-east-consistent-v1/bare-manifest.json'},'helmet':{'idle':'character/veld-helmet-fitting-east-v2/equipped-idle-manifest.json','pickup':'character/veld-pickup-east-consistent-v1/helmet-manifest.json','unload':'character/veld-unload-east-consistent-v1/helmet-manifest.json'}}
specs=[('idle',0),('pickup',-1),('unload',0),('held-master',5),('new-carry',0),('new-carry',2),('unload',2),('unload',5)]
board=Image.new('RGB',(2048,1080),'#202a30');d=ImageDraw.Draw(board);rows=[];bindings={}
for y,gear in enumerate(['bare','helmet']):
 for x,(state,index) in enumerate(specs):
  if state in ['held-master','new-carry']:
   directory=R/('character/veld-cargo-turns-master-family-v1/north-east-candidate-v5' if state=='held-master' else 'character/veld-carry-east-master-proportions-v1/paired-package-v1');path=directory/'frames'/gear/f'{index:03}.png';pivot=[128,224];manifest=None
  else:
   manifest=R/selected[gear][state];data=json.loads(manifest.read_text());entry=next(s for s in data['states'] if s['id'] in [state+'-east','equipped-idle-east']);ref=entry['frameFiles'][index];path=R/ref.removeprefix('res://') if ref.startswith('res://') else manifest.parent/ref;pivot=data['pivot']
  im=Image.open(path).convert('RGBA');canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,(128-round(pivot[0]),224-round(pivot[1])))
  d.text((x*256+5,y*540+5),gear+' '+state+' '+str(index),fill='white');board.paste(canvas,(x*256,y*540+24),canvas)
  detail=canvas.crop((80,66,179,163)).resize((248,243),Image.Resampling.NEAREST);board.paste(detail,(x*256+4,y*540+280),detail)
  a=np.array(canvas);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min());_,headx=np.where(a[top:top+20,:,3]>128)
  relative=path.relative_to(R).as_posix();bindings[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
  if manifest:bindings[manifest.relative_to(R).as_posix()]=hashlib.sha256(manifest.read_bytes()).hexdigest()
  rows.append({'gear':gear,'state':state,'index':index,'source':relative,'pivot':pivot,'opaqueTop':top,'top20WidthProxy':int(headx.max()-headx.min()+1)})
board.save(P/'east-join-audit.png')
(P/'join-review-evidence.json').write_text(json.dumps({'rows':rows,'bindings':bindings,'scope':'Current source endpoints plus staged masters/carry, pivot registration only; no actual controller join or adoption evidence.','visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'presentations':16,'headWidthProxies':[{k:v for k,v in r.items() if k in ['gear','state','index','top20WidthProxy']} for r in rows]}))
