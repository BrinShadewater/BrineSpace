from pathlib import Path
import json,copy,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];binding={};counts={}
for gear in ['bare','helmet']:
 sources=[R/f'character/veld-seated-south-coherent-v1/{gear}-manifest.json',R/f'character/veld-seated-south-breathing-v1/{gear}-manifest.json',R/f'character/veld-read-seated-south-coherent-v1/{gear}-manifest.json']
 states={};metadata=None
 for source in sources:
  data=json.loads(source.read_text());binding[source.relative_to(R).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
  profile={k:data[k] for k in ['precomposed','frameWidth','frameHeight','pivot','standingHeight','textureFilter']}
  if metadata is None:metadata=profile
  assert metadata==profile
  for s in data['states']:
   state=copy.deepcopy(s);state['frameFiles']=['res://'+(source.parent/f).relative_to(R).as_posix() for f in state['frameFiles']]
   for name in state['frameFiles']:
    f=R/name.removeprefix('res://');assert f.is_file();binding[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
   states[state['id']]=state
 out={'name':'Veld selected South seated and tablet '+gear,'status':'installed_locally_owner_review_open',**metadata,'states':list(states.values())}
 (P/f'{gear}-manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
 counts[gear]={'states':len(states),'references':sum(len(s['frameFiles']) for s in states.values())}
(P/'source-bindings.json').write_text(json.dumps({'scope':'immutable tested source composition, whole literal res paths; selection and native proof separate','bindings':binding,'counts':counts},indent=2)+'\n',encoding='utf-8')
print(json.dumps(counts))
