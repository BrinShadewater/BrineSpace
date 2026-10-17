"""Exact loop joins, reverse, native contracts and inherited transition metadata."""
from pathlib import Path
import json
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];cov=json.loads((R/'character/veld-consistency-audit-v3/coverage.json').read_text());checks=0;profiles=[]
for v in ['bare','helmet']:
 p=H/f'{v}-manifest.json'
 if not p.exists():continue
 m=json.loads(p.read_text());states={s['id']:s for s in m['states']};profiles.append(v)
 for k,expected in [('frameWidth',256),('frameHeight',256),('pivot',[128,128]),('standingHeight',148),('precomposed',True)]:assert m[k]==expected;checks+=1
 for direction in ['west-north','north-west']:
  key='swim-turn-'+direction;state=states[key];src=json.loads((R/cov['selected'][v][key]['manifest']).read_text());old=next(s for s in src['states'] if s['id']==key);assert {k:x for k,x in state.items() if k!='frameFiles'}=={k:x for k,x in old.items() if k!='frameFiles'};checks+=1
  for file in state['frameFiles']:
   im=Image.open(H/file);assert im.size==(256,256) and im.mode=='RGBA';checks+=1
  for slot,d in [(0,direction.split('-')[0]),(5,direction.split('-')[1])]:
   ref=R/f'character/veld-water-{d}-coherent-v1/frames/{v}/swim-{d}/000.png';assert Image.open(H/state['frameFiles'][slot]).tobytes()==Image.open(ref).tobytes();checks+=1
 for i in range(6):assert Image.open(H/states['swim-turn-west-north']['frameFiles'][i]).tobytes()==Image.open(H/states['swim-turn-north-west']['frameFiles'][5-i]).tobytes();checks+=1
 if v=='helmet':
  bare=json.loads((H/'bare-manifest.json').read_text());assert all({k:s[k] for k in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']}=={k:b[k] for k in ['frameDurationsMs','loop','facings','waterKinds','waterPoses','depthOffsets']} for s,b in zip(m['states'],bare['states']));checks+=1
(H/'packaging-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'profiles':profiles,'scope':'exactselectedloopjoins/reverse/nativecontracts/inheritedstateclockandwatermetadata; no motion acceptance','installed':False},indent=2)+'\n');print(f'{checks} packaging/join checks PASS; profiles {profiles}')
