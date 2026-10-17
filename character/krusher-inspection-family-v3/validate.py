from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;old=R/'character/krusher-inspection-family-v2';canon=R/'character/krusher-james-canonical-v6';checks=0;errors=[];expected={}
def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def path(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
for q in json.loads((canon/'revision.json').read_text())['records']:
 if not q['alias']:expected[q['gear'],hashlib.sha256(arr(R/q['source'][6:]).tobytes()).hexdigest()]=arr(canon/q['output'])
for gear in ['bare','helmet']:
 name=gear+'-manifest.json';before=json.loads((old/name).read_text());after=json.loads((P/name).read_text());check({k:v for k,v in before.items() if k!='states'}=={k:v for k,v in after.items() if k!='states'},'root profile exact');check(len(before['states'])==len(after['states']),'state coverage exact');idle={s['id']:s for s in json.loads((canon/name).read_text())['states']}
 for a,b in zip(before['states'],after['states']):
  check({k:v for k,v in a.items() if k!='frameFiles'}=={k:v for k,v in b.items() if k!='frameFiles'},'state clocks and flags exact');check(len(a['frameFiles'])==len(b['frameFiles']),'source count exact')
  for x,y in zip(a['frameFiles'],b['frameFiles']):
   source=arr(path(old/name,x));target=path(P/name,y);check(target.is_file(),'whole file path present');check(np.array_equal(arr(target),expected[gear,hashlib.sha256(source.tobytes()).hexdigest()]),'exact revised canonical pose association')
  d=a['id'].rsplit('-',1)[1]
  for i in [0,-1]:check(np.array_equal(arr(path(P/name,b['frameFiles'][i])),arr(path(canon/name,idle['idle-'+d]['frameFiles'][0]))),'exact idle join')
result={'checks':checks,'errors':errors,'scope':'All1146inspection references, original root/state fields/counts/clocks exactly retained except whole frame paths; independent old full RGBA association to revised canonical poses;16exact idle joins. No new artwork or station-life acceptance.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':errors}));assert not errors
