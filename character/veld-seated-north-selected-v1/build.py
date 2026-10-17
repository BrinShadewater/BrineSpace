"""Compose tested immutable North seating and breathing, whole source paths."""
from pathlib import Path
import copy,hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1]
bindings={};counts={}
for gear in ('bare','helmet'):
 states={};profile=None
 for family in ('veld-seated-north-coherent-v1','veld-seated-north-breathing-source-v1'):
  source=R/f'character/{family}/{gear}-manifest.json'
  data=json.loads(source.read_text(encoding='utf-8'))
  bindings[source.relative_to(R).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
  values={key:data[key] for key in ('precomposed','frameWidth','frameHeight','pivot','standingHeight','textureFilter')}
  if profile is None:profile=values
  assert profile==values,'compatible tested source profile'
  for original in data['states']:
   state=copy.deepcopy(original);files=[]
   for name in state['frameFiles']:
    path=R/name.removeprefix('res://') if name.startswith('res://') else source.parent/name
    assert path.is_file()
    bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    files.append('res://'+path.relative_to(R).as_posix())
   state['frameFiles']=files;states[state['id']]=state
 out={'name':f'Veld selected North seated breathing {gear}','status':'installed_locally_owner_review_open',**profile,'states':list(states.values())}
 if gear=='helmet':out['equipment']='diving-helmet'
 (P/f'{gear}-manifest.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
 counts[gear]={'states':len(states),'references':sum(len(s['frameFiles']) for s in states.values())}
(P/'source-bindings.json').write_text(json.dumps({'bindings':bindings,'counts':counts,'scope':'immutable North source composition; actual normal loader/lifecycle evidence distinct'},indent=2)+'\n',encoding='utf-8')
print(json.dumps(counts))
