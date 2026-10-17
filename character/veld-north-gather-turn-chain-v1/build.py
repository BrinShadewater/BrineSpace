from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
T=R/'character/veld-turn-north-east-helmet-aligned-v3';G=R/'character/veld-gather-north-original-master-v2';E=R/'character/veld-gather-north-original-master-v1'
bindings={};checks=0
for gear in ['bare','helmet']:
 m=json.loads((T/(gear+'-manifest.json')).read_text());g=json.loads((G/(gear+'-manifest.json')).read_text());ref='res://'+(E/'gather-frames'/gear/'000.png').relative_to(R).as_posix()
 for s in m['states']:
  s['frameFiles'][0 if s['id']=='carry-turn-north-east' else -1]=ref
  assert sum(s['frameDurationsMs'])==800;checks+=1
 m['states']+=copy.deepcopy(g['states']);m['name']='Veld corrected North gather/turn chain '+gear;m['status']='staged_not_installed'
 states={s['id']:s for s in m['states']}
 for a,b in [('carry-gather-north','carry-turn-north-east'),('carry-turn-north-east','carry-turn-east-north'),('carry-turn-east-north','carry-spread-north')]:assert states[a]['frameFiles'][-1]==states[b]['frameFiles'][0];checks+=1
 for s in m['states']:
  for path in s['frameFiles']:bindings[path[6:]]=hashlib.sha256((R/path[6:]).read_bytes()).hexdigest()
 (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
for folder in [T,G]:
 for gear in ['bare','helmet']:
  path=folder/(gear+'-manifest.json');bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'bindings':bindings,'scope':'Corrected exact North endpoint aliases and gather/turn/reverse/spread finite chain. Interior turn poses unchanged; projected footwear/body/material continuity requires native visual review.'},indent=2)+'\n',encoding='utf-8')
print(checks,'exact chain joins/timing checks0failures')
