from pathlib import Path
from PIL import Image
import json,numpy as np
P=Path(__file__).resolve().parent;OLD=P.parent/'krusher-water-cargo-turns-v1'
a={(q['gear'],q['sourceHash']):q for q in json.load(open(OLD/'provenance.json'))['records']};changed=[];same={};checks=0
for q in json.load(open(P/'provenance.json'))['records']:
 before=np.array(Image.open(OLD/a[(q['gear'],q['sourceHash'])]['output']).convert('RGBA'));after=np.array(Image.open(P/q['output']).convert('RGBA'));checks+=1
 if np.array_equal(before,after):same[q['gear']]=same.get(q['gear'],0)+1
 else:
  assert q['gear']=='bare';diff=np.any(before!=after,2);ys,xs=np.where(diff);changed.append({'gear':q['gear'],'state':q['state'],'frame':q['frame'],'pixels':int(diff.sum()),'box':[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]})
assert same['helmet']==80
q=next(q for q in json.load(open(P/'provenance.json'))['records'] if q['gear']=='bare' and q['state']=='swim-carry-turn-east-south' and q['frame']==1);after=np.array(Image.open(P/q['output']).convert('RGBA'))
for x,y in [(143,107),(144,107),(146,108),(148,109)]:
 assert after[y,x,3]==0,(x,y,after[y,x]);checks+=1
for family in ['cargo','turn','cargo-turn']:
 old=json.load(open(OLD/f'{family}-bare-manifest.json'));new=json.load(open(P/f'{family}-bare-manifest.json'))
 for a,b in zip(old['states'],new['states']):
  for i in [0,len(a['frameFiles'])-1]:
   assert np.array_equal(np.array(Image.open(OLD/a['frameFiles'][i]).convert('RGBA')),np.array(Image.open(P/b['frameFiles'][i]).convert('RGBA'))),a['id'];checks+=1
(P/'revision.json').write_text(json.dumps({'checks':checks,'errors':[],'changedUnique':changed,'unchangedUnique':same,'scope':'Bare original skull silhouette and detached fringe correction only. All80helmet unique decoded images and every state first/final pose unchanged; four verified old fringe points cleared; alpha1 pixel belonging to authored Krusher head retained. Existing foreground/collar/hardware guards retained.'},indent=2)+'\n')
im=Image.open(P/q['output']).crop((115,95,165,150)).resize((500,550),Image.Resampling.NEAREST);bg=Image.new('RGBA',im.size,'#242c31');bg.alpha_composite(im);bg.convert('RGB').save(P/'quarter-diagnostic-krusher.png')
print(json.dumps({'checks':checks,'changed':len(changed),'unchanged':same}))
